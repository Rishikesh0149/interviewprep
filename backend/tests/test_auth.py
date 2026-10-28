import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "disclaimer" in data

def test_user_registration_and_login_flow():
    test_email = "alex.rivera@example.com"
    test_password = "securePassword123!"

    # 1. Register new user
    reg_response = client.post("/api/v1/auth/register", json={
        "email": test_email,
        "password": test_password,
        "full_name": "Alex Rivera",
        "experience_level": "intermediate",
        "target_role": "Software Engineer"
    })
    assert reg_response.status_code in [201, 400]
    
    # 2. Login
    login_response = client.post("/api/v1/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "tokens" in login_data
    access_token = login_data["tokens"]["access_token"]
    refresh_token = login_data["tokens"]["refresh_token"]

    # 3. Access protected /me endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == test_email
    assert me_data["full_name"] == "Alex Rivera"

    # 4. Refresh token
    refresh_resp = client.post(f"/api/v1/auth/refresh?refresh_token_str={refresh_token}")
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json()
