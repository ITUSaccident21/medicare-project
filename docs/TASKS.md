# 📋 BẢNG PHÂN RÃ CÔNG VIỆC DỰ ÁN VITAP (WBS & NOTION TASK MATRIX)

> **Mô hình học tập từ AI Bloxorz:** Phân rã nhỏ từng chức năng đến mức độ 1 hàm / 1 file / 1 giao diện cụ thể.  
> **Nguyên tắc:** Có mã số rõ ràng (`1.x`, `2.x`, `3.x`, `4.x`), xác định rõ **Còn chờ task nào (Dependencies)** và **Đang chặn task nào (Blocks)** để cả 4 thành viên cùng phát triển song song trong Sandbox mà không bị nghẽn cổ chai.

---

## 👥 Bảng Quy Ước Mã Số & Vai Trò (Roles)

| Mã vai trò | Thành viên | Chuyên môn | Trách nhiệm trọng tâm |
| :---: | :--- | :--- | :--- |
| **VT1** | **Trương Huệ Trí** (`24120472`) | PO & Data Lead | CSDL 3NF, Auth JWT, Dataset thuốc & Hồ sơ bệnh nền |
| **VT2** | **Nguyễn Bảo Trọng** (`24120476`) | DevOps & Backend Lead | Docker, CI/CD, Gateway, Scheduler nhắc thuốc & QA |
| **VT3** | **Dương Phan Minh Trí** (`24120470`) | Frontend & DDI Lead | UI React Web, Thuật toán DDI Engine $O(N^2)$, Responsive |
| **VT4** | **Lê Thanh Phong** (`24120409`) | AI Assistant Lead | Gemini Vision OCR, ChromaDB RAG Chatbot, Guardrails |

---

## 📊 BẢNG TASK CHI TIẾT (COPY THẲNG VÀO NOTION)

| Mã | Tên Task (Chi tiết kỹ thuật) | Vai trò | Trạng thái | Sẵn sàng? | Còn chờ (Dependencies) | Đang chặn (Blocks) | Người phụ trách |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **1.1** | Tạo repo GitHub, phân quyền Sandbox & quy ước commit | `VT1 Trưởng nhóm` | **Xong** | 🟢 Đã xong | Không | 1.2, 2.1, 3.1, 4.1 | **Trương Huệ Trí** |
| **1.2** | Thiết kế Schema CSDL PostgreSQL 3NF (`app/models/`) | `VT1 Trưởng nhóm` | **Xong** | 🟢 Đã xong | 1.1 | 1.3, 1.4, 2.3, 3.2 | **Trương Huệ Trí** |
| **1.3** | Tạo Script nạp 50 hoạt chất & 100 biệt dược mẫu ban đầu | `VT1 Trưởng nhóm` | Chưa làm | 🟢 Sẵn sàng | 1.2 | 3.2, 3.8 | **Trương Huệ Trí** |
| **1.4** | Viết API Đăng ký / Đăng nhập JWT + Hash Bcrypt (`m0_auth.py`) | `VT1 Trưởng nhóm` | Chưa làm | 🟢 Sẵn sàng | 1.2 | 1.5, 3.5 | **Trương Huệ Trí** |
| **1.5** | Viết API CRUD Hồ sơ bệnh nền & Tiền sử dị ứng thuốc | `VT1 Trưởng nhóm` | Chưa làm | 🟡 Còn chờ 1 task | 1.4 | 1.6, 3.3, 3.6 | **Trương Huệ Trí** |
| **1.6** | Viết API Nhật ký chỉ số sinh hiệu (Huyết áp, Đường huyết, BMI) | `VT1 Trưởng nhóm` | Chưa làm | 🟡 Còn chờ 1 task | 1.5 | 3.6 | **Trương Huệ Trí** |
| **1.7** | Pipeline làm sạch & mở rộng Dataset 300–600 biệt dược | `VT1 Trưởng nhóm` | Chưa làm | 🟡 Còn chờ 1 task | 1.3 | Test tải dữ liệu lớn | **Trương Huệ Trí** |
| **1.8** | Viết Unit Test CSDL và Auth (`test_m0_auth.py`) | `VT1 Trưởng nhóm` | Chưa làm | 🟡 Còn chờ 1 task | 1.4, 2.3 | CI pass Sprint 1 | **Trương Huệ Trí** |
| | | | | | | | |
| **2.1** | Thiết lập Dockerfile & `docker-compose.yml` (App + Postgres) | `VT2 DevOps` | **Xong** | 🟢 Đã xong | 1.1 | 2.2, 2.8 | **Nguyễn Bảo Trọng** |
| **2.2** | Cấu hình GitHub Actions CI chạy Pytest tự động | `VT2 DevOps` | **Xong** | 🟢 Đã xong | 2.1 | 1.8, 2.7, 3.4 | **Nguyễn Bảo Trọng** |
| **2.3** | Tạo fixture Test Database và `conftest.py` chuẩn cho nhóm | `VT2 DevOps` | Chưa làm | 🟢 Sẵn sàng | 1.2 | 1.8, 2.7, 3.4 | **Nguyễn Bảo Trọng** |
| **2.4** | Xây dựng API Gateway, CORS, Global Exception Handler | `VT2 DevOps` | Chưa làm | 🟢 Sẵn sàng | 1.1 | 1.4, 3.2, 4.3 | **Nguyễn Bảo Trọng** |
| **2.5** | Lập trình Background Service Scheduler tính cữ uống thuốc | `VT2 DevOps` | Chưa làm | 🟢 Sẵn sàng | 1.1 | 2.6, 3.7 | **Nguyễn Bảo Trọng** |
| **2.6** | Viết API Lịch uống thuốc hôm nay & API đánh dấu "Đã uống" | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 1 task | 2.5 | 3.7 | **Nguyễn Bảo Trọng** |
| **2.7** | Viết Unit Test cho Gateway & Scheduler (`test_scheduler.py`) | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 2 task | 2.3, 2.5 | CI pass Sprint 2 | **Nguyễn Bảo Trọng** |
| **2.8** | Đóng gói và Deploy Backend lên Cloud (Render/Railway) | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 3 task | 2.1, 2.4, 3.2 | Demo cuối kỳ | **Nguyễn Bảo Trọng** |
| | | | | | | | |
| **3.1** | Khởi tạo React Vite + Tailwind + Mock Service Sandbox | `VT3 Frontend` | **Xong** | 🟢 Đã xong | 1.1 | 3.5, 3.6, 3.7 | **Dương Phan Minh Trí** |
| **3.2** | Viết thuật toán DDI đối kháng ma trận $O(N^2)$ (`m4_ddi.py`) | `VT3 Frontend` | Chưa làm | 🟢 Sẵn sàng | 1.2 | 3.3, 3.4, 3.8 | **Dương Phan Minh Trí** |
| **3.3** | Bổ sung logic kiểm tra Thuốc - Bệnh nền & Dị ứng chéo | `VT3 Frontend` | Chưa làm | 🟡 Còn chờ 2 task | 3.2, 1.5 | 3.8 | **Dương Phan Minh Trí** |
| **3.4** | Viết Unit Test kiểm tra ma trận tương tác (`test_m4_ddi.py`) | `VT3 Frontend` | Chưa làm | 🟡 Còn chờ 2 task | 3.2, 2.3 | CI pass Sprint 3 | **Dương Phan Minh Trí** |
| **3.5** | Lập trình giao diện Trang Đăng nhập & Đăng ký (`LoginPage.tsx`) | `VT3 Frontend` | Chưa làm | 🟢 Sẵn sàng (Mock) | 3.1 | Tích hợp Real API (1.4) | **Dương Phan Minh Trí** |
| **3.6** | Lập trình Dashboard Chỉ số sinh hiệu & Biểu đồ biến động | `VT3 Frontend` | Chưa làm | 🟢 Sẵn sàng (Mock) | 3.1 | Tích hợp Real API (1.6) | **Dương Phan Minh Trí** |
| **3.7** | Lập trình UI Tủ thuốc cá nhân & Lịch uống timeline | `VT3 Frontend` | Chưa làm | 🟢 Sẵn sàng (Mock) | 3.1 | Tích hợp Scheduler (2.6) | **Dương Phan Minh Trí** |
| **3.8** | Lập trình UI Tra cứu tương tác thuốc & Thẻ cảnh báo Đỏ/Vàng | `VT3 Frontend` | Chưa làm | 🟢 Sẵn sàng (Mock) | 3.1, 3.2 | Hoàn thiện Module F2 | **Dương Phan Minh Trí** |
| **3.9** | Tối ưu Mobile UI Responsive & Triển khai Vercel | `VT3 Frontend` | Chưa làm | 🟡 Còn chờ 3 task | 3.5, 3.7, 3.8 | Demo sản phẩm | **Dương Phan Minh Trí** |
| | | | | | | | |
| **4.1** | Thử nghiệm bóc tách ảnh đơn thuốc bằng Gemini Vision | `VT4 AI Lead` | Chưa làm | 🟢 Sẵn sàng | 1.1 | 4.2 | **Lê Thanh Phong** |
| **4.2** | Xây dựng Prescription OCR Engine (`services/ocr/scanner.py`) | `VT4 AI Lead` | Chưa làm | 🟡 Còn chờ 1 task | 4.1 | 4.3, 3.7 | **Lê Thanh Phong** |
| **4.3** | Viết API upload ảnh đơn thuốc & chuẩn hóa sang danh mục CSDL | `VT4 AI Lead` | Chưa làm | 🟡 Còn chờ 2 task | 4.2, 1.3 | Tủ thuốc nhận diện OCR | **Lê Thanh Phong** |
| **4.4** | Thu thập & làm sạch tài liệu y tế Bộ Y tế (Dinh dưỡng, Tập luyện) | `VT4 AI Lead` | Chưa làm | 🟢 Sẵn sàng | Không | 4.5 | **Lê Thanh Phong** |
| **4.5** | Xây dựng ChromaDB Local Vector Store & Pipeline nhúng ngữ nghĩa | `VT4 AI Lead` | Chưa làm | 🟡 Còn chờ 1 task | 4.4 | 4.6 | **Lê Thanh Phong** |
| **4.6** | Xây dựng RAG Chatbot y tế kèm Prompt Guardrails & Trích dẫn | `VT4 AI Lead` | Chưa làm | 🟡 Còn chờ 1 task | 4.5 | 4.7, 4.8 | **Lê Thanh Phong** |
| **4.7** | Viết API hỏi đáp sức khỏe `/api/v1/chatbot` & Test an toàn | `VT4 AI Lead` | Chưa làm | 🟡 Còn chờ 1 task | 4.6 | CI pass Sprint 3 | **Lê Thanh Phong** |
| **4.8** | Lập trình Component ChatBox React có trích dẫn nguồn y tế | `VT4 AI Lead` | Chưa làm | 🟡 Còn chờ 1 task | 4.6, 3.1 | Hoàn thiện Phân hệ F3 | **Lê Thanh Phong** |
