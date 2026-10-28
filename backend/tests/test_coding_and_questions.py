import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    test_email = "code.tester@example.com"
    test_password = "securePassword123!"

    client.post("/api/v1/auth/register", json={
        "email": test_email,
        "password": test_password,
        "full_name": "Devin Coder",
        "experience_level": "intermediate",
        "target_role": "Software Engineer"
    })

    login_resp = client.post("/api/v1/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    token = login_resp.json()["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_coding_problems():
    resp = client.get("/api/v1/coding/problems")
    assert resp.status_code == 200
    problems = resp.json()
    assert len(problems) >= 3
    assert any(p["id"] == "two-sum" for p in problems)


def test_get_coding_problem_details():
    resp = client.get("/api/v1/coding/problems/two-sum")
    assert resp.status_code == 200
    problem = resp.json()
    assert problem["title"] == "Two Sum"
    assert "starter_code" in problem
    assert "examples" in problem
    assert "constraints" in problem


def test_run_code_sandbox():
    valid_solution = """
def twoSum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []
"""
    resp = client.post("/api/v1/coding/run", json={
        "problem_id": "two-sum",
        "language": "python",
        "code": valid_solution
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ["Passed", "Success"]
    assert data["passed_cases"] > 0


def test_submit_code_solution(auth_headers):
    valid_solution = """
def twoSum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
"""
    resp = client.post("/api/v1/coding/submit", json={
        "problem_id": "two-sum",
        "language": "python",
        "code": valid_solution
    }, headers=auth_headers)
    assert resp.status_code == 200
    sub_data = resp.json()
    assert sub_data["status"] == "Passed"
    assert sub_data["passed_cases"] > 0

    # Verify history
    history_resp = client.get("/api/v1/coding/submissions", headers=auth_headers)
    assert history_resp.status_code == 200
    subs = history_resp.json()
    assert any(s["problem_id"] == "two-sum" for s in subs)


def test_browse_question_bank():
    # 1. Fetch question list
    resp = client.get("/api/v1/questions")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    assert len(data["questions"]) > 0
    first_q = data["questions"][0]
    assert "question_text" in first_q
    assert "ideal_star_answer" in first_q

    # 2. Fetch single question
    detail_resp = client.get(f"/api/v1/questions/{first_q['id']}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == first_q["id"]

    # 3. Filter by search
    search_resp = client.get("/api/v1/questions?search=system")
    assert search_resp.status_code == 200
