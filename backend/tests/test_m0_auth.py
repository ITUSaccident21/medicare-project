"""
Module M0 Sandbox Tests: Xác thực & Quản lý Tài khoản / Hồ sơ bệnh nhân
Phụ trách chính (Owner): VT1 - Trương Huệ Trí (MSSV: 24120472)
Quy tắc: Thành viên khác KHÔNG tự ý chỉnh sửa file test này.
"""

def test_m0_login_success(client):
    """Kiểm tra M0: Đăng nhập thành công trả về access token."""
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "mock_token"
