# 📋 BẢNG PHÂN RÃ CÔNG VIỆC DỰ ÁN VITAP (NOTION TASK MATRIX)

> **Mô hình chuẩn hóa từ dự án AI Bloxorz:**  
> - Phân rã nhỏ đến mức độ từng hàm, từng model CSDL, từng component UI riêng biệt.  
> - Đảm bảo nguyên tắc **Vertical Slice**: Mỗi thành viên làm trọn gói từ UI đến Backend, không ai phải ngồi đợi ai.  
> - Có sẵn file CSV để nhập trực tiếp vào Notion: [`docs/notion_tasks_import.csv`](notion_tasks_import.csv).

---

## 👥 Bảng Phân Chia 4 Lát Cắt Tính Năng (Vertical Slices)

| Lát cắt | Thành viên | Vai trò trên Notion | Trách nhiệm trọn gói từ A ➔ Z |
| :---: | :--- | :--- | :--- |
| **Slice 1 (1.x)** | **Trương Huệ Trí** (`24120472`) | `VT1 Hồ sơ & Sinh hiệu` | UI Dashboard cá nhân + API Auth JWT + CSDL 3NF + Biểu đồ biến thiên Huyết áp/Đường huyết |
| **Slice 2 (2.x)** | **Nguyễn Bảo Trọng** (`24120476`) | `VT2 Tủ thuốc & Nhắc nhở` | UI Tủ thuốc & Timeline + API CRUD Tủ thuốc + Thuật toán Scheduler nhắc cữ uống + DevOps CI/CD |
| **Slice 3 (3.x)** | **Dương Phan Minh Trí** (`24120470`) | `VT3 Tương tác Dược lý` | UI Tìm kiếm thuốc & Cảnh báo + Thuật toán DDI $O(N^2)$ + Đối kháng Thuốc-Bệnh nền + Gemini dặn dò |
| **Slice 4 (4.x)** | **Lê Thanh Phong** (`24120409`) | `VT4 Trợ lý AI & OCR` | UI ChatBox trích dẫn nguồn + ChromaDB RAG Y tế + Gemini Vision bóc tách đơn thuốc OCR |

---

## 📊 BẢNG TASK CHI TIẾT (COPY HOẶC IMPORT VÀO NOTION)

| Mã | Task (Tên việc cụ thể) | Vai trò | Trạng thái | Sẵn sàng? | Còn chờ | Đang chặn | Người làm |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **1.0** | Tạo repo GitHub, phân quyền Sandbox & quy ước commit | `VT1 Hồ sơ & Sinh hiệu` | **Xong** | 🟢 Đã xong | | 1.1, 2.0, 3.0, 4.0 | Trương Huệ Trí |
| **1.1** | Thiết kế Schema CSDL 3NF chung trên PostgreSQL | `VT1 Hồ sơ & Sinh hiệu` | **Xong** | 🟢 Đã xong | 1.0 | 1.2, 2.3, 3.1 | Trương Huệ Trí |
| **1.2** | Viết Model SQLAlchemy User & PatientProfile | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.1 | 1.3, 1.4 | Trương Huệ Trí |
| **1.3** | Viết API Đăng ký & Đăng nhập (Bcrypt + JWT Token) | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟡 Còn chờ 1 task | 1.2 | 1.6 | Trương Huệ Trí |
| **1.4** | Viết API CRUD Hồ sơ bệnh nhân (Bệnh nền & Tiền sử dị ứng) | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟡 Còn chờ 1 task | 1.2 | 1.7, 3.4 | Trương Huệ Trí |
| **1.5** | Viết Model HealthVital & API ghi nhận chỉ số (Huyết áp, Đường huyết, BMI) | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟡 Còn chờ 1 task | 1.4 | 1.8 | Trương Huệ Trí |
| **1.6** | Giao diện React: Trang Đăng nhập & Đăng ký (LoginPage.tsx) | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟢 Sẵn sàng bắt đầu | | 1.9 | Trương Huệ Trí |
| **1.7** | Giao diện React: Dashboard Hồ sơ cá nhân & Form nhập chỉ số sinh hiệu | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟡 Còn chờ 1 task | 1.6 | 1.8 | Trương Huệ Trí |
| **1.8** | Giao diện React: Biểu đồ đường biến thiên huyết áp & đường huyết (Recharts) | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟡 Còn chờ 2 task | 1.5, 1.7 | | Trương Huệ Trí |
| **1.9** | Viết bộ 8 Unit Test luồng Auth và ghi nhận chỉ số (test_m0_auth.py) | `VT1 Hồ sơ & Sinh hiệu` | Chưa làm | 🟡 Còn chờ 2 task | 1.3, 2.2 | | Trương Huệ Trí |
| | | | | | | | |
| **2.0** | Thiết lập Dockerfile & docker-compose chạy FastAPI + PostgreSQL | `VT2 Tủ thuốc & Nhắc nhở` | **Xong** | 🟢 Đã xong | 1.0 | 2.1, 2.2 | Nguyễn Bảo Trọng |
| **2.1** | Cấu hình GitHub Actions CI tự động chạy Pytest | `VT2 Tủ thuốc & Nhắc nhở` | **Xong** | 🟢 Đã xong | 2.0 | 1.9, 2.10, 3.5, 4.7 | Nguyễn Bảo Trọng |
| **2.2** | Tạo fixture Test Database in-memory và conftest.py chuẩn | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 2.0 | 1.9, 2.10, 3.5 | Nguyễn Bảo Trọng |
| **2.3** | Thiết kế bảng CSDL user_cabinets (tủ thuốc & liều dùng) | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.1 | 2.4 | Nguyễn Bảo Trọng |
| **2.4** | Viết API CRUD Tủ thuốc cá nhân (Thêm/Sửa/Xóa thuốc đang uống) | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟡 Còn chờ 1 task | 2.3 | 2.5, 2.7 | Nguyễn Bảo Trọng |
| **2.5** | Viết thuật toán Scheduler tính cữ uống trong ngày (Sáng/Trưa/Tối) | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟡 Còn chờ 1 task | 2.4 | 2.6 | Nguyễn Bảo Trọng |
| **2.6** | Viết API lấy Lịch uống thuốc hôm nay & API đánh dấu "Đã uống" | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟡 Còn chờ 1 task | 2.5 | 2.8 | Nguyễn Bảo Trọng |
| **2.7** | Giao diện React: Màn hình Tủ thuốc cá nhân (CabinetPage.tsx) | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟢 Sẵn sàng bắt đầu | | 2.8 | Nguyễn Bảo Trọng |
| **2.8** | Giao diện React: Widget Timeline cữ uống & nút tích "Đã uống" | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟡 Còn chờ 2 task | 2.6, 2.7 | 2.9 | Nguyễn Bảo Trọng |
| **2.9** | Tích hợp Popup Web Notification API thông báo nhắc giờ uống thuốc | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟡 Còn chờ 1 task | 2.8 | | Nguyễn Bảo Trọng |
| **2.10** | Viết bộ test tự động cho Scheduler và sinh lịch uống (test_scheduler.py) | `VT2 Tủ thuốc & Nhắc nhở` | Chưa làm | 🟡 Còn chờ 2 task | 2.2, 2.5 | | Nguyễn Bảo Trọng |
| | | | | | | | |
| **3.0** | Thử nghiệm thuật toán đối kháng cặp hoạt chất trong sandbox | `VT3 Tương tác Dược lý` | **Xong** | 🟢 Đã xong | 1.0 | 3.2 | Dương Phan Minh Trí |
| **3.1** | Nạp bộ dữ liệu ban đầu 50 hoạt chất & 100 biệt dược mẫu (data_seed) | `VT3 Tương tác Dược lý` | Chưa làm | 🟢 Sẵn sàng bắt đầu | 1.1 | 3.2, 4.2 | Dương Phan Minh Trí |
| **3.2** | Viết thuật toán DDI đối kháng ma trận O(N^2) trong m4_ddi.py | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 2 task | 3.0, 3.1 | 3.3, 3.5 | Dương Phan Minh Trí |
| **3.3** | Bổ sung cơ chế phân cấp rủi ro Đỏ (Nguy hiểm) / Vàng (Thận trọng) / Xanh | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 1 task | 3.2 | 3.4, 3.8 | Dương Phan Minh Trí |
| **3.4** | Bổ sung logic kiểm tra Thuốc - Bệnh nền & Dị ứng chéo theo hồ sơ | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 2 task | 3.3, 1.4 | 3.6, 3.8 | Dương Phan Minh Trí |
| **3.5** | Viết bộ 15 Unit Test ma trận tương tác cặp hoạt chất (test_m4_ddi.py) | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 2 task | 2.2, 3.2 | | Dương Phan Minh Trí |
| **3.6** | Tích hợp Gemini 1.5 Flash cá nhân hóa lời cảnh báo dược lý an toàn | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 1 task | 3.4 | 3.8 | Dương Phan Minh Trí |
| **3.7** | Giao diện React: Ô tìm kiếm Autocomplete biệt dược & giỏ thuốc kiểm tra | `VT3 Tương tác Dược lý` | Chưa làm | 🟢 Sẵn sàng bắt đầu | | 3.8 | Dương Phan Minh Trí |
| **3.8** | Giao diện React: Màn hình kết quả cảnh báo Đỏ/Vàng/Xanh & Modal cơ chế | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 3 task | 3.3, 3.6, 3.7 | 3.9 | Dương Phan Minh Trí |
| **3.9** | Tích hợp nút "Kiểm tra tương tác toàn bộ tủ thuốc" từ CSDL của VT2 | `VT3 Tương tác Dược lý` | Chưa làm | 🟡 Còn chờ 2 task | 2.4, 3.8 | | Dương Phan Minh Trí |
| | | | | | | | |
| **4.0** | Thử nghiệm Gemini Vision bóc tách ảnh đơn thuốc trong sandbox | `VT4 Trợ lý AI & OCR` | **Xong** | 🟢 Đã xong | 1.0 | 4.1 | Lê Thanh Phong |
| **4.1** | Xây dựng Prescription OCR Engine bóc tách tên thuốc và hàm lượng | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 1 task | 4.0 | 4.2 | Lê Thanh Phong |
| **4.2** | Viết API Upload ảnh đơn thuốc & chuẩn hóa sang danh mục CSDL | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 2 task | 4.1, 3.1 | 4.9 | Lê Thanh Phong |
| **4.3** | Thu thập & làm sạch 15 trang tài liệu dinh dưỡng Bộ Y tế (Markdown) | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟢 Sẵn sàng bắt đầu | | 4.4 | Lê Thanh Phong |
| **4.4** | Xây dựng ChromaDB Local Vector Store & pipeline Embedding văn bản | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 1 task | 4.3 | 4.5 | Lê Thanh Phong |
| **4.5** | Xây dựng RAG Chatbot kết hợp Gemini 1.5 Flash trả lời có trích dẫn nguồn | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 1 task | 4.4 | 4.6, 4.8 | Lê Thanh Phong |
| **4.6** | Cài đặt Safety Guardrails: từ chối kê đơn và cảnh báo tham khảo bác sĩ | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 1 task | 4.5 | 4.7 | Lê Thanh Phong |
| **4.7** | Viết API hỏi đáp y tế /api/v1/chatbot & Unit Test kiểm tra an toàn prompt | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 2 task | 2.2, 4.6 | | Lê Thanh Phong |
| **4.8** | Giao diện React: Component ChatBox hội thoại thông minh có trích dẫn nguồn | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 1 task | 4.5 | | Lê Thanh Phong |
| **4.9** | Giao diện React: Nút bấm & Modal chụp/upload ảnh đơn thuốc vào Tủ thuốc | `VT4 Trợ lý AI & OCR` | Chưa làm | 🟡 Còn chờ 2 task | 4.2, 2.7 | | Lê Thanh Phong |

---

## 🚀 HƯỚNG DẪN IMPORT VÀO NOTION TRONG 10 GIÂY

1. Mở trang Notion của bạn.
2. Bấm vào nút `...` (hoặc `Settings`) ở góc trên bên phải trang Notion ➔ chọn **Import** ➔ chọn **CSV**.
3. Chọn file [`docs/notion_tasks_import.csv`](notion_tasks_import.csv) nằm trong project.
4. Notion sẽ tự động tạo một Database đầy đủ các cột: **Mã, Task, Vai trò, Trạng thái, Sẵn sàng?, Còn chờ, Đang chặn, Người làm** y hệt như dự án mẫu Bloxorz!
