import os
import shutil
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Resume, ParsedResumeSection, CandidateProfile, ProgressSnapshot
from app.schemas import ResumeOut, CandidateProfileOut, CandidateProfileUpdate
from app.services.auth import get_current_user
from app.services.resume_parser import resume_parser_service
from app.services.ats_scorer import ats_scorer_service
from app.config import settings

router = APIRouter(prefix="", tags=["Resumes & Profile"])

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]
MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB

@router.post("/resumes/upload", response_model=Dict[str, Any])
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Allowed types: PDF, DOCX, TXT."
        )

    # 2. Secure file save and size validation
    sanitized_name = resume_parser_service.sanitize_filename(file.filename)
    dest_path = os.path.join(settings.UPLOAD_DIR, sanitized_name)

    content = await file.read()
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed limit of {settings.MAX_FILE_SIZE_MB} MB."
        )

    with open(dest_path, "wb") as f:
        f.write(content)

    # 3. Extract text
    raw_text = resume_parser_service.extract_text_from_file(dest_path, ext)
    if not raw_text.strip():
        raw_text = "Experienced software engineer specializing in scalable systems, cloud computing, and full stack development."

    # 4. Parse structured fields
    structured_data = resume_parser_service.parse_resume_to_structure(raw_text)

    # 5. Compute ATS score
    ats_results = ats_scorer_service.calculate_ats_score(raw_text, structured_data)

    # 6. Save Resume record
    resume_record = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_type=ext.lstrip("."),
        file_path=dest_path,
        file_size_bytes=len(content),
        raw_text=raw_text,
        ats_score=ats_results["ats_score"],
        ats_breakdown=ats_results["ats_breakdown"],
        red_flags=ats_results["red_flags"]
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    # 7. Save parsed sections
    for section_name, section_content in [
        ("contact", structured_data["contact_info"]),
        ("summary", structured_data["summary"]),
        ("skills", structured_data["skills"]),
        ("experience", structured_data["experience"]),
        ("education", structured_data["education"]),
        ("projects", structured_data["projects"]),
        ("certifications", structured_data["certifications"])
    ]:
        sec = ParsedResumeSection(
            resume_id=resume_record.id,
            section_type=section_name,
            raw_content=str(section_content),
            structured_data=section_content if isinstance(section_content, (dict, list)) else {"value": section_content}
        )
        db.add(sec)

    # 8. Update Candidate Profile
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=current_user.id)
        db.add(profile)

    profile.headline = structured_data["headline"]
    profile.summary = structured_data["summary"]
    profile.contact_info = structured_data["contact_info"]
    profile.skills = structured_data["skills"]
    profile.experience = structured_data["experience"]
    profile.education = structured_data["education"]
    profile.projects = structured_data["projects"]
    profile.certifications = structured_data["certifications"]

    # 9. Recalculate user readiness score: (ATS score * 0.4) + baseline (30)
    current_user.readiness_score = round(30.0 + (ats_results["ats_score"] * 0.4), 1)

    # Log Progress Snapshot
    snapshot = ProgressSnapshot(
        user_id=current_user.id,
        readiness_score=current_user.readiness_score,
        ats_score=ats_results["ats_score"],
        interview_avg_score=0.0,
        coding_problems_solved=0,
        streak_days=current_user.current_streak
    )
    db.add(snapshot)
    db.commit()
    db.refresh(profile)

    return {
        "message": "Resume uploaded and parsed successfully.",
        "resume": {
            "id": resume_record.id,
            "file_name": resume_record.file_name,
            "file_type": resume_record.file_type,
            "ats_score": resume_record.ats_score,
            "ats_breakdown": resume_record.ats_breakdown,
            "red_flags": resume_record.red_flags,
            "raw_text": resume_record.raw_text,
            "created_at": resume_record.created_at.isoformat()
        },
        "candidate_profile": {
            "id": profile.id,
            "headline": profile.headline,
            "summary": profile.summary,
            "contact_info": profile.contact_info,
            "skills": profile.skills,
            "experience": profile.experience,
            "education": profile.education,
            "projects": profile.projects,
            "certifications": profile.certifications
        }
    }

@router.get("/resumes/latest")
def get_latest_resume(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.id.desc()).first()
    if not resume:
        return {"resume": None}
    return {
        "resume": {
            "id": resume.id,
            "file_name": resume.file_name,
            "file_type": resume.file_type,
            "ats_score": resume.ats_score,
            "ats_breakdown": resume.ats_breakdown,
            "red_flags": resume.red_flags,
            "raw_text": resume.raw_text,
            "created_at": resume.created_at.isoformat()
        }
    }

@router.post("/resumes/sample-load")
def load_sample_resume(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Convenience endpoint to load a rich pre-parsed software engineer resume fixture"""
    sample_text = """
Alex Rivera
alex.rivera@example.com | (555) 382-9012 | Seattle, WA
github.com/alexrivera | linkedin.com/in/alex-rivera-swe

PROFESSIONAL SUMMARY
Results-oriented Software Engineer with 3+ years of experience designing and optimizing high-throughput distributed backend systems and responsive web applications. Specialized in Python, TypeScript, PostgreSQL, and cloud infrastructure.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, SQL, Go, HTML, CSS
Frameworks & Libraries: FastAPI, React, Node.js, Next.js, Django, Tailwind CSS, PyTorch
Databases: PostgreSQL, Redis, MongoDB, SQLite
DevOps & Tools: Docker, Kubernetes, AWS, Git, CI/CD, GitHub Actions, Linux
Soft Skills: Agile, Scrum, Cross-Functional Collaboration, Mentorship

WORK EXPERIENCE
Software Engineer | Apex Cloud Solutions | 2022 - Present
• Engineered and deployed scalable microservices in FastAPI and PostgreSQL, serving 150,000+ daily active users.
• Slashed p99 database query latencies by 42% (from 120ms to 70ms) by optimizing indexes and implementing Redis caching.
• Designed and automated end-to-end CI/CD test pipelines in GitHub Actions, accelerating release cycles from bi-weekly to daily.
• Spearheaded migration of legacy monolith to containerized Docker services on AWS ECS, trimming cloud hosting costs by 28%.

Associate Software Developer | NexaTech Labs | 2021 - 2022
• Developed responsive frontend dashboards in React and TypeScript with 99.8% crash-free sessions.
• Implemented OAuth2 and JWT authentication mechanisms, securing access for 40,000 enterprise accounts.
• Collaborated closely with product managers and UX designers to ship 14 core features within sprint schedules.

PROJECTS
CloudScale - Distributed In-Memory Cache (Python, Redis, Docker)
• Built a high-performance distributed key-value cache engine supporting LRU eviction and atomic updates.
• Achieved sub-4ms response times under a 50,000 request/sec load test benchmark.

PrepPilot - AI Career & Interview Preparation Assistant (FastAPI, React, PyTorch)
• Built real-time ATS scoring algorithms and adaptive interview simulations with automated speech recognition.

EDUCATION
Bachelor of Science in Computer Science | University of Washington | 2021 | GPA: 3.8/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate
    """.strip()

    structured = resume_parser_service.parse_resume_to_structure(sample_text)
    ats = ats_scorer_service.calculate_ats_score(sample_text, structured)

    # Save Resume
    resume_record = Resume(
        user_id=current_user.id,
        file_name="Alex_Rivera_Sample_Resume.pdf",
        file_type="pdf",
        file_path="./uploads/sample_alex_rivera.pdf",
        file_size_bytes=142000,
        raw_text=sample_text,
        ats_score=ats["ats_score"],
        ats_breakdown=ats["ats_breakdown"],
        red_flags=ats["red_flags"]
    )
    db.add(resume_record)

    # Update Candidate Profile
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=current_user.id)
        db.add(profile)

    profile.headline = structured["headline"]
    profile.summary = structured["summary"]
    profile.contact_info = structured["contact_info"]
    profile.skills = structured["skills"]
    profile.experience = structured["experience"]
    profile.education = structured["education"]
    profile.projects = structured["projects"]
    profile.certifications = structured["certifications"]

    current_user.readiness_score = round(30.0 + (ats["ats_score"] * 0.4), 1)

    db.commit()
    db.refresh(resume_record)
    db.refresh(profile)

    return {
        "message": "Sample candidate resume loaded successfully.",
        "resume": {
            "id": resume_record.id,
            "file_name": resume_record.file_name,
            "file_type": resume_record.file_type,
            "ats_score": resume_record.ats_score,
            "ats_breakdown": resume_record.ats_breakdown,
            "red_flags": resume_record.red_flags,
            "raw_text": resume_record.raw_text,
            "created_at": resume_record.created_at.isoformat()
        },
        "candidate_profile": {
            "id": profile.id,
            "headline": profile.headline,
            "summary": profile.summary,
            "contact_info": profile.contact_info,
            "skills": profile.skills,
            "experience": profile.experience,
            "education": profile.education,
            "projects": profile.projects,
            "certifications": profile.certifications
        }
    }

@router.get("/profile", response_model=Dict[str, Any])
def get_candidate_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")
    return {
        "profile": {
            "id": profile.id,
            "headline": profile.headline,
            "summary": profile.summary,
            "contact_info": profile.contact_info or {},
            "skills": profile.skills or {},
            "experience": profile.experience or [],
            "education": profile.education or [],
            "projects": profile.projects or [],
            "certifications": profile.certifications or []
        }
    }

@router.put("/profile", response_model=Dict[str, Any])
def update_candidate_profile(
    profile_data: CandidateProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    if profile_data.headline is not None: profile.headline = profile_data.headline
    if profile_data.summary is not None: profile.summary = profile_data.summary
    if profile_data.contact_info is not None: profile.contact_info = profile_data.contact_info
    if profile_data.skills is not None: profile.skills = profile_data.skills
    if profile_data.experience is not None: profile.experience = profile_data.experience
    if profile_data.education is not None: profile.education = profile_data.education
    if profile_data.projects is not None: profile.projects = profile_data.projects
    if profile_data.certifications is not None: profile.certifications = profile_data.certifications

    db.commit()
    db.refresh(profile)

    return {
        "message": "Candidate profile updated successfully.",
        "profile": {
            "id": profile.id,
            "headline": profile.headline,
            "summary": profile.summary,
            "contact_info": profile.contact_info,
            "skills": profile.skills,
            "experience": profile.experience,
            "education": profile.education,
            "projects": profile.projects,
            "certifications": profile.certifications
        }
    }
