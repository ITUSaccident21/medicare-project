from fastapi import APIRouter
router = APIRouter()

@router.get("/{specialty_id}")
def get_checklist(specialty_id: int):
    return {"required_documents": ["CCCD", "Thẻ BHYT"], "notes": "Nhịn ăn sáng nếu xét nghiệm máu"}
