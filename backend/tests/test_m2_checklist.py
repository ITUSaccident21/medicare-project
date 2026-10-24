"""
Module M2 Sandbox Tests: Hướng dẫn chuẩn bị trước khám & Khai báo triệu chứng
Phụ trách chính (Owner): VT2 - Nguyễn Bảo Trọng (MSSV: 24120476)
Quy tắc: Thành viên khác KHÔNG tự ý chỉnh sửa file test này.
"""

def test_m2_get_specialty_checklist(client):
    """Kiểm tra M2: Lấy danh mục giấy tờ và lưu ý y tế theo chuyên khoa."""
    response = client.get("/api/v1/checklist/1")
    assert response.status_code == 200
    data = response.json()
    assert "required_documents" in data
    assert isinstance(data["required_documents"], list)
