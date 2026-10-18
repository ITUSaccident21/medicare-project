from fastapi import APIRouter
router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Stub M0: Đăng nhập thành công", "access_token": "mock_token"}
