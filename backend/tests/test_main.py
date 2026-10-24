def test_root_endpoint(client):
    """Kiểm tra healthcheck endpoint gốc."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "MediCare API" in data["message"]
