"""
Module M5 Sandbox Tests: Phiếu Tổng hợp Tiền khám & Mã QR Bác sĩ
Phụ trách chính (Owner): VT1 - Trương Huệ Trí (MSSV: 24120472)
Quy tắc: Thành viên khác KHÔNG tự ý chỉnh sửa file test này.
"""

def test_m5_get_previsit_summary(client):
    """Kiểm tra M5: Trích xuất phiếu tóm tắt tiền khám kèm mã QR."""
    response = client.get("/api/v1/summary/101")
    assert response.status_code == 200
    data = response.json()
    assert data["appointment_id"] == 101
    assert "qr_code_url" in data
