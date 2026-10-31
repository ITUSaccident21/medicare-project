"""
Unit tests cho thuật toán Fuzzy Matching (Task 1.5).
Phụ trách chính: VT1 - Trương Huệ Trí (MSSV: 24120472)
"""

import pytest
from app.models.drug_models import BrandName, ActiveIngredient
from app.services.fuzzy_matcher import match_drug_name

@pytest.fixture(scope="function", autouse=True)
def seed_test_drugs(db_session):
    """Nạp một số thuốc mẫu vào test database in-memory."""
    p_ing = ActiveIngredient(inn_name="Paracetamol", drug_class="Giảm đau")
    i_ing = ActiveIngredient(inn_name="Ibuprofen", drug_class="Kháng viêm")
    db_session.add_all([p_ing, i_ing])
    db_session.flush()

    panadol = BrandName(brand_name="Panadol Extra", dosage_form="Viên nén")
    gofen = BrandName(brand_name="Gofen 400", dosage_form="Viên nang mềm")
    db_session.add_all([panadol, gofen])
    db_session.commit()

def test_fuzzy_match_exact(db_session):
    """Kiểm tra tìm kiếm khớp chính xác 100%."""
    res = match_drug_name("Panadol Extra", db_session)
    assert res.match_status == "EXACT_MATCH"
    assert res.best_match_name == "Panadol Extra"
    assert res.confidence >= 0.95

def test_fuzzy_match_typo(db_session):
    """Kiểm tra tìm kiếm khớp gần đúng khi người dùng/OCR gõ sai nhẹ."""
    # "Panadol Extr" thiếu chữ a
    res = match_drug_name("Panadol Extr", db_session)
    assert res.match_status in ("EXACT_MATCH", "FUZZY_MATCH")
    assert res.best_match_name == "Panadol Extra"
    assert res.confidence >= 0.85

def test_fuzzy_match_active_ingredient(db_session):
    """Kiểm tra so khớp theo tên hoạt chất gốc."""
    res = match_drug_name("Paracetamol", db_session)
    assert res.best_match_name == "Paracetamol"
    assert not res.is_brand
    assert res.confidence >= 0.95

def test_fuzzy_match_unmatched(db_session):
    """Kiểm tra chuỗi ký tự rác không nhận diện được trả về UNMATCHED."""
    res = match_drug_name("Kha123_random_text_abc", db_session)
    assert res.match_status == "UNMATCHED"
    assert res.best_match_id is None
