import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """
    TestClient dùng chung cho toàn bộ test suite.
    """
    with TestClient(app) as test_client:
        yield test_client
