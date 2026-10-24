## 📌 Thông Tin Pull Request

### 1. Mã Task & Liên kết Issue
- **Sprint / Task**: <!-- Ví dụ: Sprint 1 - Task 1.2 / M0 Auth -->
- **Liên kết Issue**: Closes #<!-- Số issue nếu có, ví dụ: Closes #5 -->

### 2. Loại Thay Đổi
- [ ] `feat`: Thêm tính năng / endpoint / giao diện mới
- [ ] `fix`: Sửa lỗi logic / bug API hoặc UI
- [ ] `test`: Bổ sung hoặc cập nhật kịch bản kiểm thử
- [ ] `refactor`: Tối ưu mã nguồn (không đổi chức năng)
- [ ] `docs`: Soạn hoặc cập nhật tài liệu (SRS, SDD, README...)
- [ ] `chore`: Cấu hình, dependencies, seed data

---

## 📝 Tóm Tắt Nội Dung Đã Làm
<!-- Mô tả ngắn gọn 3-5 gạch đầu dòng về những gì bạn đã cài đặt hoặc chỉnh sửa -->
- 

---

## 🧪 Hướng Dẫn Kiểm Thử (Testing Instructions)
<!-- Ghi rõ các bước để Reviewer có thể kiểm tra trên máy của họ -->
1. Chạy lệnh:
   ```bash
   cd backend
   pytest tests/ -v
   ```
2. Thao tác kiểm tra trên Swagger UI hoặc Postman:
   - Endpoint: `POST /api/v1/...`
   - Payload mẫu:
     ```json
     {}
     ```
   - Kết quả mong đợi:

---

## 👥 Phân Công Reviewer
- **Reviewer chính**: <!-- @tag_ten_thanh_vien theo bảng CONTRIBUTING.md -->
- **Reviewer dự phòng**: 

---

## ✅ Checklist Tự Kiểm Tra Trước Khi Yêu Cầu Review
- [ ] Mã nguồn chỉ nằm trong phạm vi module / thư mục được phân công.
- [ ] Không có file nhạy cảm lọt vào git (`.env`, `GEMINI_API_KEY`, tokens, file tạm).
- [ ] Đã chạy test nội bộ và toàn bộ test đều xanh (PASS).
- [ ] Không làm gãy API Contract đã thống nhất với Frontend / Backend.
- [ ] Đã cập nhật `requirements.txt` hoặc `package.json` nếu có cài thêm thư viện mới.
