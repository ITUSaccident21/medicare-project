from fastapi import APIRouter
router = APIRouter()

@router.post("/tickets")
def book_ticket():
    return {"ticket_number": 42, "slot": "08:00 - 09:00", "status": "CONFIRMED"}
