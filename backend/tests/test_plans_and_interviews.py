import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    test_email = "test.interview@example.com"
    test_password = "securePassword123!"

    # Register or login
    client.post("/api/v1/auth/register", json={
        "email": test_email,
        "password": test_password,
        "full_name": "Jordan Lee",
        "experience_level": "intermediate",
        "target_role": "Software Engineer"
    })

    login_resp = client.post("/api/v1/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    token = login_resp.json()["tokens"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_target_roles_and_gap_report(auth_headers):
    # 1. Fetch roles
    roles_resp = client.get("/api/v1/roles")
    assert roles_resp.status_code == 200
    roles = roles_resp.json()
    assert len(roles) >= 1
    assert any("Software Engineer" in r["title"] for r in roles)

    # 2. Get skill gap report
    gap_resp = client.get("/api/v1/gap-report", headers=auth_headers)
    assert gap_resp.status_code == 200
    gap_data = gap_resp.json()
    assert "match_percentage" in gap_data
    assert "strong_skills" in gap_data
    assert "recommendations" in gap_data
    assert len(gap_data["recommendations"]) > 0


def test_study_plan_generation_and_task_toggle(auth_headers):
    # 1. Generate study plan
    gen_resp = client.post("/api/v1/plans/generate", json={
        "role_title": "Software Engineer",
        "hours_per_day": 2.5,
        "total_weeks": 4
    }, headers=auth_headers)
    assert gen_resp.status_code == 200
    plan = gen_resp.json()
    assert plan["total_weeks"] == 4
    assert len(plan["tasks"]) > 0
    first_task = plan["tasks"][0]
    assert first_task["tier"] in ["BASIC", "INTERMEDIATE", "ADVANCED"]

    # 2. Get current plan
    curr_resp = client.get("/api/v1/plans/current", headers=auth_headers)
    assert curr_resp.status_code == 200
    assert curr_resp.json()["id"] == plan["id"]

    # 3. Toggle task completion
    toggle_resp = client.patch(f"/api/v1/plans/tasks/{first_task['id']}/toggle", headers=auth_headers)
    assert toggle_resp.status_code == 200
    updated_plan = toggle_resp.json()
    updated_task = next(t for t in updated_plan["tasks"] if t["id"] == first_task["id"])
    assert updated_task["is_completed"] is True
    assert updated_plan["progress_percentage"] > 0


def test_mock_interview_flow(auth_headers):
    # 1. Start interview simulation
    start_resp = client.post("/api/v1/interviews/start", json={
        "role_title": "Software Engineer",
        "level": 2,
        "persona": "Technical Lead",
        "mode": "text",
        "round_type": "Technical"
    }, headers=auth_headers)
    assert start_resp.status_code == 200
    session_data = start_resp.json()
    assert session_data["status"] == "in_progress"
    assert len(session_data["turns"]) == 1
    turn1 = session_data["turns"][0]
    assert len(turn1["question_text"]) > 10

    # 2. Submit candidate answer
    answer_resp = client.post("/api/v1/interviews/turn/answer", json={
        "turn_id": turn1["id"],
        "answer_text": "In my previous project, we faced high latency on our order processing endpoint. I profiled our database queries, discovered missing composite indexes on user_id and created_at, and introduced Redis caching. As a result, our p99 response times dropped by 45% and system throughput increased to 2,500 req/s.",
        "audio_duration_sec": 35.0,
        "filler_word_count": 1,
        "speaking_wpm": 130.0
    }, headers=auth_headers)
    assert answer_resp.status_code == 200
    turn_feedback_data = answer_resp.json()
    assert len(turn_feedback_data["turns"]) >= 1
    eval_turn = turn_feedback_data["turns"][0]
    assert eval_turn["feedback"] is not None
    assert eval_turn["feedback"]["score_overall"] >= 6.0
    assert len(eval_turn["feedback"]["sample_ideal_answer"]) > 0

    # 3. Complete interview session
    complete_resp = client.post(f"/api/v1/interviews/{session_data['id']}/complete", headers=auth_headers)
    assert complete_resp.status_code == 200
    final_data = complete_resp.json()
    assert final_data["status"] == "completed"
    assert final_data["overall_score"] > 0
    assert len(final_data["strengths"]) > 0
    assert len(final_data["weaknesses"]) > 0
    assert len(final_data["suggested_topics_to_improve"]) > 0

    # 4. List user interviews
    list_resp = client.get("/api/v1/interviews", headers=auth_headers)
    assert list_resp.status_code == 200
    all_sessions = list_resp.json()
    assert any(s["id"] == session_data["id"] for s in all_sessions)
