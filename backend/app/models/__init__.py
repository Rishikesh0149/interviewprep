import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    experience_level = Column(String(50), default="intermediate") # beginner, intermediate, senior
    target_role = Column(String(100), default="Software Engineer")
    readiness_score = Column(Float, default=0.0)
    current_streak = Column(Integer, default=1)
    last_active_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    gap_reports = relationship("SkillGapReport", back_populates="user", cascade="all, delete-orphan")
    interviews = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    coding_submissions = relationship("CodingSubmission", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("Badge", back_populates="user", cascade="all, delete-orphan")
    progress_snapshots = relationship("ProgressSnapshot", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False) # pdf, docx, txt
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    raw_text = Column(Text, default="")
    ats_score = Column(Float, default=0.0)
    ats_breakdown = Column(JSON, default=dict) # breakdown by metrics
    red_flags = Column(JSON, default=list)
    tailored_version = Column(Text, nullable=True) # improved resume text/json
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    sections = relationship("ParsedResumeSection", back_populates="resume", cascade="all, delete-orphan")


class ParsedResumeSection(Base):
    __tablename__ = "parsed_resume_sections"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    section_type = Column(String(50), nullable=False) # contact, summary, education, experience, projects, skills, certifications
    raw_content = Column(Text, default="")
    structured_data = Column(JSON, default=dict)

    resume = relationship("Resume", back_populates="sections")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    headline = Column(String(255), default="")
    summary = Column(Text, default="")
    contact_info = Column(JSON, default=dict) # email, phone, location, linkedin, github, portfolio
    skills = Column(JSON, default=dict) # languages, frameworks, databases, tools, soft_skills
    experience = Column(JSON, default=list) # [{company, role, start, end, bullets}]
    education = Column(JSON, default=list) # [{institution, degree, field, grad_year, gpa}]
    projects = Column(JSON, default=list) # [{name, tech_stack, description, live_url, repo_url}]
    certifications = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class TargetRole(Base):
    __tablename__ = "target_roles"

    id = Column(Integer, primary_key=True, index=True)
    role_key = Column(String(100), unique=True, nullable=False) # e.g. software_engineer, ml_engineer
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Engineering")
    description = Column(Text, default="")
    required_skills = Column(JSON, default=list)
    nice_to_have_skills = Column(JSON, default=list)
    core_competencies = Column(JSON, default=list)
    typical_interview_rounds = Column(JSON, default=list)

    questions = relationship("QuestionBank", back_populates="role", cascade="all, delete-orphan")


class SkillGapReport(Base):
    __tablename__ = "skill_gap_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_title = Column(String(255), nullable=False)
    match_percentage = Column(Float, default=0.0)
    strong_skills = Column(JSON, default=list)
    partial_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="gap_reports")


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_title = Column(String(255), nullable=False)
    total_weeks = Column(Integer, default=4)
    hours_per_day = Column(Float, default=2.0)
    target_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active") # active, completed, archived
    progress_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="study_plans")
    tasks = relationship("StudyTask", back_populates="plan", cascade="all, delete-orphan")


class StudyTask(Base):
    __tablename__ = "study_tasks"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    day_number = Column(Integer, nullable=False)
    tier = Column(String(50), default="BASIC") # BASIC, INTERMEDIATE, ADVANCED
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    topic = Column(String(100), default="General")
    resource_type = Column(String(50), default="article") # article, video, practice, quiz
    resource_url = Column(String(500), default="")
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    plan = relationship("StudyPlan", back_populates="tasks")


class QuestionBank(Base):
    __tablename__ = "question_bank"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("target_roles.id"), nullable=True)
    level = Column(Integer, default=1) # 1=Foundation, 2=Intermediate, 3=Advanced
    category = Column(String(100), default="Technical") # Technical, Behavioral, System Design, HR, Coding
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(50), default="Medium") # Easy, Medium, Hard
    expected_keywords = Column(JSON, default=list)
    ideal_star_answer = Column(Text, default="")
    rubric_hints = Column(JSON, default=list)

    role = relationship("TargetRole", back_populates="questions")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_title = Column(String(255), default="Software Engineer")
    mode = Column(String(50), default="text") # text, voice, timed_round
    persona = Column(String(50), default="Technical Lead") # Friendly, Strict, Technical Lead, Panel
    round_type = Column(String(50), default="Technical") # HR, Technical, System Design, Full-Round
    level = Column(Integer, default=2) # 1, 2, 3
    status = Column(String(50), default="in_progress") # in_progress, completed
    overall_score = Column(Float, default=0.0) # 0 to 10
    total_turns = Column(Integer, default=0)
    summary_feedback = Column(Text, default="")
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    suggested_topics_to_improve = Column(JSON, default=list)
    wpm_average = Column(Float, default=0.0)
    filler_words_total = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="interviews")
    turns = relationship("InterviewTurn", back_populates="session", cascade="all, delete-orphan")


class InterviewTurn(Base):
    __tablename__ = "interview_turns"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    turn_index = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    question_category = Column(String(100), default="Technical")
    user_answer = Column(Text, default="")
    audio_duration_sec = Column(Float, default=0.0)
    filler_word_count = Column(Integer, default=0)
    speaking_wpm = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("InterviewSession", back_populates="turns")
    feedback = relationship("Feedback", back_populates="turn", uselist=False, cascade="all, delete-orphan")


class Feedback(Base):
    __tablename__ = "turn_feedback"

    id = Column(Integer, primary_key=True, index=True)
    turn_id = Column(Integer, ForeignKey("interview_turns.id"), unique=True, nullable=False)
    score_overall = Column(Float, default=7.0)
    score_relevance = Column(Float, default=7.0)
    score_star_structure = Column(Float, default=7.0)
    score_technical_accuracy = Column(Float, default=7.0)
    score_clarity = Column(Float, default=7.0)
    score_confidence = Column(Float, default=7.0)
    score_conciseness = Column(Float, default=7.0)
    critique = Column(Text, default="")
    sample_ideal_answer = Column(Text, default="")
    detected_weak_points = Column(JSON, default=list)

    turn = relationship("InterviewTurn", back_populates="feedback")


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String(100), nullable=False)
    problem_title = Column(String(255), nullable=False)
    language = Column(String(50), default="python") # python, javascript
    code_content = Column(Text, nullable=False)
    passed_cases = Column(Integer, default=0)
    total_cases = Column(Integer, default=0)
    runtime_ms = Column(Float, default=0.0)
    status = Column(String(50), default="Passed") # Passed, Failed, SyntaxError
    ai_feedback = Column(Text, default="")
    time_complexity = Column(String(50), default="O(N)")
    space_complexity = Column(String(50), default="O(1)")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="coding_submissions")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_key = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    icon = Column(String(100), default="award")
    tier = Column(String(50), default="Bronze") # Bronze, Silver, Gold, Platinum
    earned_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="badges")


class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    readiness_score = Column(Float, default=0.0)
    ats_score = Column(Float, default=0.0)
    interview_avg_score = Column(Float, default=0.0)
    coding_problems_solved = Column(Integer, default=0)
    streak_days = Column(Integer, default=1)
    snapshot_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="progress_snapshots")
