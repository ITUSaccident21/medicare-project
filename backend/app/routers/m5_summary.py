from fastapi import APIRouter
router = APIRouter()

@router.get("/{appointment_id}")
def get_previsit_summary(appointment_id: int):
    return {
        "appointment_id": appointment_id,
        "summary": "Phiếu tóm tắt tiền khám 1 trang",
        "qr_code_url": "data:image/png;base64,stub"
    }
