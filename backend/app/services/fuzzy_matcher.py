"""
Dịch vụ So khớp Mờ (Fuzzy Matching Service) cho Module OCR & Autocomplete.
Phụ trách chính (Owner): VT1 - Trương Huệ Trí (MSSV: 24120472)
Người phối hợp: VT3 - Dương Phan Minh Trí

Mục tiêu:
- Nhận chuỗi ký tự nhận diện từ ảnh đơn thuốc (OCR) hoặc ô tìm kiếm người dùng.
- Chuẩn hóa chuỗi (xóa dấu cách thừa, chuyển chữ thường, tách biệt hàm lượng).
- So khớp với toàn bộ Biệt dược (BrandName) và Hoạt chất (ActiveIngredient) trong CSDL.
- Phân loại độ tin cậy:
    + EXACT_MATCH: Điểm tương đồng >= 0.95
    + FUZZY_MATCH: Điểm tương đồng >= 0.65 (trả kèm danh sách gợi ý candidates)
    + UNMATCHED:   Điểm tương đồng < 0.65
"""

import re
from difflib import SequenceMatcher
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.models.drug_models import BrandName, ActiveIngredient

class MatchCandidate(BaseModel):
    drug_id: int
    name: str
    is_brand: bool
    score: float

class FuzzyMatchResult(BaseModel):
    raw_query: str
    best_match_id: Optional[int] = None
    best_match_name: Optional[str] = None
    is_brand: bool = True
    confidence: float = 0.0
    match_status: str = "UNMATCHED"  # EXACT_MATCH | FUZZY_MATCH | UNMATCHED
    candidates: List[MatchCandidate] = Field(default_factory=list)

def clean_drug_name(text: str) -> str:
    """Loại bỏ ký tự đặc biệt, chuẩn hóa khoảng trắng để so khớp chuẩn."""
    text = text.lower().strip()
    # Loại bỏ dấu câu không cần thiết
    text = re.sub(r"[^\w\s]", " ", text)
    # Gom các khoảng trắng thừa
    text = re.sub(r"\s+", " ", text).strip()
    return text

def calculate_similarity(s1: str, s2: str) -> float:
    """Tính toán điểm tương đồng giữa hai chuỗi theo thuật toán SequenceMatcher."""
    clean1 = clean_drug_name(s1)
    clean2 = clean_drug_name(s2)
    if clean1 == clean2:
        return 1.0
    # So khớp trực tiếp chuỗi con
    if clean1 in clean2 or clean2 in clean1:
        base_score = len(min(clean1, clean2, key=len)) / len(max(clean1, clean2, key=len))
        seq_score = SequenceMatcher(None, clean1, clean2).ratio()
        return max(base_score * 0.95, seq_score)
    return SequenceMatcher(None, clean1, clean2).ratio()

def match_drug_name(query: str, db: Session, limit: int = 5) -> FuzzyMatchResult:
    """
    So khớp chuỗi `query` với toàn bộ BrandName và ActiveIngredient trong CSDL.
    Trả về cấu trúc FuzzyMatchResult phục vụ xác nhận đơn thuốc.
    """
    query_clean = clean_drug_name(query)
    if not query_clean:
        return FuzzyMatchResult(raw_query=query, match_status="UNMATCHED")

    all_candidates: List[MatchCandidate] = []

    # 1. Quét bảng BrandName
    brands = db.query(BrandName.id, BrandName.brand_name).all()
    for b_id, b_name in brands:
        score = calculate_similarity(query_clean, b_name)
        if score >= 0.50:
            all_candidates.append(MatchCandidate(
                drug_id=b_id,
                name=b_name,
                is_brand=True,
                score=round(score, 3)
            ))

    # 2. Quét bảng ActiveIngredient
    ingredients = db.query(ActiveIngredient.id, ActiveIngredient.inn_name).all()
    for ing_id, ing_name in ingredients:
        score = calculate_similarity(query_clean, ing_name)
        if score >= 0.50:
            all_candidates.append(MatchCandidate(
                drug_id=ing_id,
                name=ing_name,
                is_brand=False,
                score=round(score, 3)
            ))

    # Sắp xếp các ứng viên giảm dần theo điểm tương đồng
    all_candidates.sort(key=lambda x: x.score, reverse=True)
    top_candidates = all_candidates[:limit]

    if not top_candidates or top_candidates[0].score < 0.65:
        return FuzzyMatchResult(
            raw_query=query,
            match_status="UNMATCHED",
            confidence=top_candidates[0].score if top_candidates else 0.0,
            candidates=top_candidates
        )

    best = top_candidates[0]
    match_status = "EXACT_MATCH" if best.score >= 0.95 else "FUZZY_MATCH"

    return FuzzyMatchResult(
        raw_query=query,
        best_match_id=best.drug_id,
        best_match_name=best.name,
        is_brand=best.is_brand,
        confidence=best.score,
        match_status=match_status,
        candidates=top_candidates
    )
