from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import m0_auth, m2_checklist, m3_chatbot, m4_ddi, m5_summary

app = FastAPI(
    title="MediCare API",
    description="Hệ thống Hỗ trợ Thăm khám, Tra cứu Tương tác Thuốc & Tư vấn Sức khỏe",
    version="1.0.0"
)

# Cấu hình CORS để Frontend React gọi được API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các Routers tương ứng 6 Module
app.include_router(m0_auth.router, prefix="/api/v1/auth", tags=["M0 - Tài khoản & Hồ sơ"])
app.include_router(m2_checklist.router, prefix="/api/v1/checklist", tags=["M2 - Hướng dẫn chuẩn bị"])
app.include_router(m3_chatbot.router, prefix="/api/v1/chatbot", tags=["M3 - Trợ lý Sức khỏe AI"])
app.include_router(m4_ddi.router, prefix="/api/v1/ddi", tags=["M4 - Tương tác thuốc"])
app.include_router(m5_summary.router, prefix="/api/v1/summary", tags=["M5 - Phiếu tiền khám & QR"])

@app.get("/")
def read_root():
    return {"status": "success", "message": "MediCare API is running healthy!"}
