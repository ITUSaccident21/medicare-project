# MediCare / VitaP - Sổ Tay Y Tế Cá Nhân Hóa & Hỗ Trợ Khám Trực Tuyến

**Đồ án môn học:** Nhập môn Công nghệ Phần mềm (NMCNPM) - FIT, Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM  
**Nhóm tác giả (4 thành viên):**
- **Trương Huệ Trí** (`24120472`) - Product Owner & Data Core Lead (VT1)
- **Nguyễn Bảo Trọng** (`24120476`) - Full Stack Developer, DevOps & QA Lead (VT2)
- **Dương Phan Minh Trí** (`24120470`) - Frontend Lead & DDI Logic Lead (VT3)
- **Lê Thanh Phong** (`24120409`) - AI Assistant & Knowledge Base Lead (VT4)

---

## 🏛️ Kiến Trúc Dự Án (Phân Quyền & Sandbox Độc Lập)

Dự án áp dụng mô hình phân chia theo **File Ownership Matrix** và **Sandbox Modules** học tập từ dự án AI Bloxorz nhằm đảm bảo mỗi thành viên có không gian phát triển độc lập, không bị chồng chéo mã nguồn và không xảy ra merge conflict:

```text
0_medicare/
├── backend/                            # 📦 MÃ NGUỒN BACKEND (FastAPI + PostgreSQL)
│   ├── app/
│   │   ├── core/                       # Cấu hình hệ thống, DB connection, JWT Security (VT2)
│   │   ├── models/                     # Lược đồ CSDL SQLAlchemy 3NF & Pydantic Schemas (VT1)
│   │   ├── routers/                    # 5 Module REST API (m0_auth, m2_checklist, m3_chatbot, m4_ddi, m5_summary)
│   │   └── services/                   # Scheduler nhắc thuốc, RAG Engine, OCR Scanner (VT2 & VT4)
│   ├── data_seed/                      # Dữ liệu 350 biệt dược & Script nạp CSDL (VT1)
│   ├── tests/                          # 🧪 Test Suite Pytest phân chia theo từng module cá nhân
│   └── sandbox/                        # 🔬 Góc thử nghiệm code nháp an toàn (vt1_data_lab, vt2_devops_lab, vt3_ui_lab, vt4_ai_lab)
│
├── frontend/                           # 🖥️ MÃ NGUỒN FRONTEND (React Vite + Tailwind CSS) (VT3)
│   ├── src/pages/                      # Màn hình chính (Login, Cabinet, Interaction, Chatbot, Summary)
│   ├── src/components/                 # Components tái sử dụng (ChatBox, Modal, Buttons)
│   ├── src/services/                   # API Client tự động chuyển đổi giữa Real API và Mock Sandbox
│   └── sandbox/                        # Góc thử nghiệm giao diện nháp (prototype_ui)
│
├── docs/                               # 📚 Tài liệu kỹ thuật: SDD, SRS, UML, Test Plans
└── scripts/                            # 🔒 Script kiểm tra vi phạm commit độc lập (check_commit_scope.py)
```

---

## 🚀 Hướng Dẫn Chạy Môi Trường Phát Triển (Local Setup)

### 1. Khởi chạy Backend (FastAPI):
```bash
cd backend
python -m venv venv
source venv/bin/activate       # Trên Linux/macOS (hoặc venv\Scripts\activate trên Windows)
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`
- Chạy test kiểm thử tự động (Sandbox):
  ```bash
  pytest tests/ -v
  ```

### 2. Khởi chạy Frontend (React + Vite):
```bash
cd frontend
npm install
npm run dev
```
- Ứng dụng chạy tại: `http://localhost:5173`
- Để chạy chế độ **Mock Sandbox độc lập** không cần Backend, chỉ cần đặt `VITE_USE_MOCK=true` trong file `.env`.

---

## 📋 Quy Định Đóng Góp (Git & PR Workflow)
Vui lòng đọc kỹ file [CONTRIBUTING.md](CONTRIBUTING.md) trước khi bắt đầu tạo nhánh hoặc commit code:
- **Nguyên tắc sống còn:** *"Chỉ sửa file của mình. Cần sửa file người khác thì nhắn người đó."*
- **Commit độc lập:** Kiểm tra trước khi commit bằng lệnh `python scripts/check_commit_scope.py --staged --module <mã_module>`.
