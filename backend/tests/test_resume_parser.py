import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.resume_parser import resume_parser_service
from app.services.ats_scorer import ats_scorer_service

client = TestClient(app)

def test_resume_parser_heuristics():
    sample_text = """
    Jane Doe
    jane.doe@example.com | (555) 234-5678 | San Francisco, CA
    linkedin.com/in/janedoe | github.com/janedoe

    SUMMARY
    Senior Full Stack Engineer with 5+ years of experience building distributed systems.

    SKILLS
    Languages: Python, TypeScript, SQL, Go
    Frameworks: FastAPI, React, Next.js, Django
    Databases: PostgreSQL, Redis, MongoDB
    Tools: Docker, Kubernetes, AWS, Git

    EXPERIENCE
    Lead Backend Engineer - CloudScale Inc. (2021 - Present)
    • Architected microservices with FastAPI, improving throughput by 45%.
    • Reduced API p99 latency from 180ms to 40ms by implementing Redis caching.
    • Managed a team of 4 engineers and automated CI/CD deployments.

    EDUCATION
    University of California, Berkeley
    Bachelor of Science in Computer Science (2020)
    """

    data = resume_parser_service.parse_resume_to_structure(sample_text)
    assert data["contact_info"]["email"] == "jane.doe@example.com"
    assert "janedoe" in data["contact_info"]["linkedin"]
    assert "Python" in data["skills"]["languages"]
    assert "PostgreSQL" in data["skills"]["databases"]
    assert len(data["experience"]) > 0

    ats = ats_scorer_service.calculate_ats_score(sample_text, data)
    assert ats["ats_score"] > 60.0
    assert "ats_breakdown" in ats
    assert "quantified_impact" in ats["ats_breakdown"]

def test_resume_sample_load_and_profile_api():
    # Login as demo user
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "alex.rivera@example.com",
        "password": "securePassword123!"
    })
    token = login_resp.json()["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Load sample resume
    load_resp = client.post("/api/v1/resumes/sample-load", headers=headers)
    assert load_resp.status_code == 200
    res_data = load_resp.json()
    assert "resume" in res_data
    assert "candidate_profile" in res_data
    assert res_data["resume"]["ats_score"] > 50

    # Get profile
    prof_resp = client.get("/api/v1/profile", headers=headers)
    assert prof_resp.status_code == 200
    profile = prof_resp.json()["profile"]
    assert len(profile["skills"]["languages"]) > 0

    # Update profile
    update_resp = client.put("/api/v1/profile", json={
        "headline": "Staff AI & Systems Architect",
        "summary": "Specialized in distributed AI inference and high-scale backends."
    }, headers=headers)
    assert update_resp.status_code == 200
    updated_prof = update_resp.json()["profile"]
    assert updated_prof["headline"] == "Staff AI & Systems Architect"
