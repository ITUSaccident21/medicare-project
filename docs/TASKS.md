# 📋 BẢNG ĐẶC TẢ NHIỆM VỤ DỰ ÁN VITAP (DEFINITIVE NOTION TASK MATRIX)

> **Mô hình chuẩn hóa:** Lấy cảm hứng từ bảng quản lý phân rã độc lập của dự án mẫu AI Bloxorz.  
> **Quy chuẩn kiến trúc:**  
> - **Cơ sở dữ liệu:** Supabase PostgreSQL chuẩn 3NF (tích hợp extension `pgvector` cho RAG và `pg_trgm` cho tìm kiếm mờ).  
> - **OCR Đơn thuốc:** Hợp tác 2 pha (VT3 phụ trách nén ảnh Client-side & gọi Gemini Vision; VT1 phụ trách Fuzzy Matching map vào CSDL; Modal Human-in-the-loop xác nhận trên UI).  
> - **Tra cứu DDI:** Chuẩn hóa Canonical Pair (`drug_a_id < drug_b_id`) với Single-Shot Query chạy < 3ms.  
> - **Nhắc nhở cữ thuốc:** Cảnh báo 2 lớp (Lớp 1: In-app Banner/Audio trên Web; Lớp 2: Web Notification).  
> - **Chatbot RAG:** SSE Streaming chữ theo thời gian thực + tiêm Profile bệnh nền vào System Prompt + Fallback Cache.

---

## 👥 Ma Trận Phân Vai 4 Thành Viên

| Thành viên | Vai trò chính | Trách nhiệm trọng tâm |
| :--- | :--- | :--- |
| **Trương Huệ Trí** (`24120472`) | **PO & Data Core Lead (VT1)** | CSDL Supabase 3NF, Auth JWT, Hồ sơ Bệnh nền/Dị ứng, Dataset 300–600 thuốc, Logic Fuzzy Match OCR. |
| **Nguyễn Bảo Trọng** (`24120476`) | **Backend Lead & DevOps (VT2)** | FastAPI Gateway, Docker, CI/CD Pytest, CRUD Tủ thuốc cá nhân, Timeline cữ uống & Cảnh báo nhắc nhở 2 lớp. |
| **Dương Phan Minh Trí** (`24120470`) | **Frontend Lead & AI Vision (VT3)** | Framework React UI, Thuật toán DDI Canonical Pair $O(N^2)$, Pipeline Gemini Vision OCR, Thẻ cảnh báo Đỏ/Vàng/Xanh. |
| **Lê Thanh Phong** (`24120409`) | **ML Engineer & RAG Lead (VT4)** | Kho tri thức cẩm nang Bộ Y tế, Vector Embeddings trên Supabase `pgvector`, Safety Guardrails, ChatBox SSE Streaming. |

---

## 📊 BẢNG TASK CHI TIẾT 

| Mã | Tên Task (Kèm chi tiết kỹ thuật thực thi) | Vai trò | Trạng thái | Sẵn sàng? | Còn chờ | Đang chặn | Người làm chính | Phối hợp |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **1.0** | Tạo repo GitHub, phân quyền Sandbox & quy ước commit | `VT1 Data Core` | **Xong** | 🟢 Đã xong | | 1.1, 2.0, 3.0, 4.0 | Trương Huệ Trí | |
| **1.1** | Thiết kế Schema CSDL 3NF chung trên Supabase (bật `pgvector`, `pg_trgm`) | `VT1 Data Core` | **Xong** | 🟢 Đã xong | 1.0 | 1.2, 1.4, 2.3, 3.1, 4.2 | Trương Huệ Trí | |
| **1.2** | Viết Model SQLAlchemy & API Auth JWT (Đăng ký / Đăng nhập) | `VT1 Data Core` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.1 | 1.3, 1.6 | Trương Huệ Trí | |
| **1.3** | Viết API CRUD Hồ sơ bệnh nền & Tiền sử dị ứng thuốc | `VT1 Data Core` | Chưa làm | 🟡 Còn chờ 1 task | 1.2 | 1.6, 3.3, 4.3 | Trương Huệ Trí | |
| **1.4** | Chuẩn hóa Dataset 300–600 thuốc & nạp seed data vào Supabase | `VT1 Data Core` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.1 | 1.5, 3.1, 3.2 | Trương Huệ Trí | |
| **1.5** | Xây dựng thuật toán Fuzzy Matching so khớp chuỗi tên thuốc vào CSDL | `VT1 Data Core` | Chưa làm | 🟡 Còn chờ 1 task | 1.4 | 3.6 | Trương Huệ Trí | Dương Phan Minh Trí |
| **1.6** | UI React: Trang Đăng nhập & Form cập nhật Bệnh nền / Dị ứng | `VT1 Data Core` | Chưa làm | 🟡 Còn chờ 2 task | 1.3, 3.0 | | Trương Huệ Trí | Dương Phan Minh Trí |
| | | | | | | | | |
| **2.0** | Thiết lập Dockerfile & docker-compose chạy FastAPI + Supabase URL | `VT2 DevOps` | **Xong** | 🟢 Đã xong | 1.0 | 2.1, 2.2 | Nguyễn Bảo Trọng | |
| **2.1** | Cấu hình GitHub Actions CI tự động chạy Pytest | `VT2 DevOps` | **Xong** | 🟢 Đã xong | 2.0 | 2.7, 3.4, 4.5 | Nguyễn Bảo Trọng | |
| **2.2** | Tạo database test fixture in-memory trong `conftest.py` | `VT2 DevOps` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 2.0 | 2.7, 3.4, 4.5 | Nguyễn Bảo Trọng | |
| **2.3** | Thiết kế bảng `user_cabinets` & API CRUD Tủ thuốc gia đình | `VT2 DevOps` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.1 | 2.4, 2.5 | Nguyễn Bảo Trọng | |
| **2.4** | Viết thuật toán sinh cữ uống Sáng/Trưa/Tối & API tick "Đã uống" | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 1 task | 2.3 | 2.5, 2.6 | Nguyễn Bảo Trọng | |
| **2.5** | UI React: Màn hình Tủ thuốc cá nhân & Timeline cữ uống | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 2 task | 2.3, 2.4 | 2.6 | Nguyễn Bảo Trọng | Dương Phan Minh Trí |
| **2.6** | Tích hợp Cảnh báo nhắc uống 2 lớp: In-app Banner/Audio + Web Push | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 1 task | 2.5 | | Nguyễn Bảo Trọng | |
| **2.7** | Viết bộ Unit Test kiểm thử Tủ thuốc & Lịch uống (`test_cabinet.py`) | `VT2 DevOps` | Chưa làm | 🟡 Còn chờ 2 task | 2.2, 2.4 | | Nguyễn Bảo Trọng | |
| | | | | | | | | |
| **3.0** | Khởi tạo React Vite, Tailwind, Layout Navbar & Theme chung | `VT3 Frontend/AI` | **Xong** | 🟢 Đã xong | 1.0 | 1.6, 2.5, 3.7, 4.4 | Dương Phan Minh Trí | |
| **3.1** | Viết thuật toán DDI Canonical Pair (`ID_A < ID_B`) Single-Shot Query | `VT3 Frontend/AI` | Chưa làm | 🟡 Còn chờ 1 task | 1.4 | 3.2, 3.3, 3.4 | Dương Phan Minh Trí | |
| **3.2** | Bổ sung cơ chế phân cấp rủi ro Đỏ (Nguy hiểm) / Vàng (Thận trọng) / Xanh | `VT3 Frontend/AI` | Chưa làm | 🟡 Còn chờ 1 task | 3.1 | 3.7 | Dương Phan Minh Trí | |
| **3.3** | Bổ sung logic đối kháng: Thuốc - Bệnh nền & Thuốc - Dị ứng chéo | `VT3 Frontend/AI` | Chưa làm | 🟡 Còn chờ 2 task | 3.1, 1.3 | 3.7 | Dương Phan Minh Trí | |
| **3.4** | Viết bộ 15 Unit Test ma trận tương tác thuốc (`test_m4_ddi.py`) | `VT3 Frontend/AI` | Chưa làm | 🟡 Còn chờ 2 task | 3.1, 2.2 | | Dương Phan Minh Trí | |
| **3.5** | Tích hợp nén ảnh Client-side & gọi Gemini Vision ép Pydantic JSON | `VT3 Frontend/AI` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.0 | 3.6 | Dương Phan Minh Trí | Trương Huệ Trí |
| **3.6** | UI React: Modal xem trước đơn thuốc & Xác nhận trước khi nạp Tủ | `VT3 Frontend/AI` | Chưa làm | 🟡 Còn chờ 2 task | 3.5, 1.5 | 2.3 | Dương Phan Minh Trí | Trương Huệ Trí |
| **3.7** | UI React: Màn hình Tra cứu thuốc & Thẻ cảnh báo Đỏ/Vàng/Xanh tức thì | `VT3 Frontend/AI` | Chưa làm | 🟡 Còn chờ 3 task | 3.0, 3.2, 3.3 | | Dương Phan Minh Trí | |
| | | | | | | | | |
| **4.0** | Sandbox thử nghiệm gọi Gemini API với tài liệu cẩm nang y tế mẫu | `VT4 ML/RAG` | **Xong** | 🟢 Đã xong | 1.0 | 4.1 | Lê Thanh Phong | |
| **4.1** | Biên soạn cẩm nang dinh dưỡng & lối sống y tế dạng Markdown | `VT4 ML/RAG` | Chưa làm | 🟢 Sẵn sàng bắt đầu | | 4.2 | Lê Thanh Phong | |
| **4.2** | Xây dựng RAG Pipeline nhúng vector vào Supabase `pgvector` kèm Fallback | `VT4 ML/RAG` | Chưa làm | 🟡 Còn chờ 2 task | 4.1, 1.1 | 4.3 | Lê Thanh Phong | |
| **4.3** | Cài đặt Prompt Guardrails & Tiêm Profile bệnh nền vào System Prompt | `VT4 ML/RAG` | Chưa làm | 🟡 Còn chờ 2 task | 4.2, 1.3 | 4.4, 4.5 | Lê Thanh Phong | |
| **4.4** | UI React: Component ChatBox thông minh hỗ trợ SSE Streaming | `VT4 ML/RAG` | Chưa làm | 🟡 Còn chờ 2 task | 4.3, 3.0 | | Lê Thanh Phong | Dương Phan Minh Trí |
| **4.5** | Viết API `/api/v1/chatbot` & Unit Test kiểm tra an toàn y khoa | `VT4 ML/RAG` | Chưa làm | 🟡 Còn chờ 2 task | 4.3, 2.2 | | Lê Thanh Phong | |

---


