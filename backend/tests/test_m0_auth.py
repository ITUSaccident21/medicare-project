"""
Module M0 Sandbox Tests: Xác thực & Quản lý Tài khoản / Hồ sơ bệnh nhân
Phụ trách chính (Owner): VT1 - Trương Huệ Trí (MSSV: 24120472)
"""

def test_register_success(client):
    """Kiểm tra M0: Đăng ký tài khoản mới thành công."""
    payload = {
        "phone_number": "0912345678",
        "full_name": "Nguyễn Văn Bệnh Nhân",
        "password": "matkhauantoan123"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["full_name"] == payload["full_name"]
    assert data["phone_number"] == payload["phone_number"]

def test_register_duplicate_phone(client):
    """Kiểm tra M0: Đăng ký trùng số điện thoại bị từ chối với mã 400."""
    payload = {
        "phone_number": "0988888888",
        "full_name": "Trương Huệ Trí",
        "password": "password123"
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert "đã được đăng ký" in res2.json()["detail"]

def test_login_success(client):
    """Kiểm tra M0: Đăng nhập thành công trả về access token."""
    # Đăng ký trước
    client.post("/api/v1/auth/register", json={
        "phone_number": "0909090909",
        "full_name": "Lê Thị Khỏe",
        "password": "securepassword"
    })

    # Đăng nhập
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "0909090909",
        "password": "securepassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_credentials(client):
    """Kiểm tra M0: Đăng nhập sai mật khẩu bị từ chối với mã 401."""
    client.post("/api/v1/auth/register", json={
        "phone_number": "0933333333",
        "full_name": "Người Dùng",
        "password": "correct_password"
    })

    response = client.post("/api/v1/auth/login", json={
        "phone_number": "0933333333",
        "password": "wrong_password"
    })
    assert response.status_code == 401

def test_profile_lifecycle(client):
    """Kiểm tra M0: Vòng đời hồ sơ bệnh nền & dị ứng (Get -> Update -> Verify)."""
    # 1. Đăng ký lấy token
    reg_res = client.post("/api/v1/auth/register", json={
        "phone_number": "0977777777",
        "full_name": "Trần Văn A",
        "password": "mypassword"
    })
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Lấy hồ sơ ban đầu
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    profile_data = me_res.json()
    assert profile_data["full_name"] == "Trần Văn A"
    assert profile_data["allergies"] == ""
    assert profile_data["underlying_conditions"] == ""

    # 3. Cập nhật bệnh nền và tiền sử dị ứng thuốc
    update_res = client.put("/api/v1/auth/me/profile", headers=headers, json={
        "age": 55,
        "gender": "MALE",
        "allergies": "Penicillin, Aspirin",
        "underlying_conditions": "Cao huyết áp, Đái tháo đường type 2",
        "is_pregnant": False
    })
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["age"] == 55
    assert updated_data["gender"] == "MALE"
    assert updated_data["allergies"] == "Penicillin, Aspirin"
    assert updated_data["underlying_conditions"] == "Cao huyết áp, Đái tháo đường type 2"

    # 4. Kiểm tra lại /me thấy dữ liệu mới được lưu vĩnh viễn
    verify_res = client.get("/api/v1/auth/me", headers=headers)
    assert verify_res.status_code == 200
    assert verify_res.json()["allergies"] == "Penicillin, Aspirin"

def test_unauthenticated_profile_access(client):
    """Kiểm tra M0: Truy cập profile khi không có token bị từ chối 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
