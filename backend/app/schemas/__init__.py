from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- AUTH SCHEMAS ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    experience_level: Optional[str] = "intermediate"
    target_role: Optional[str] = "Software Engineer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    experience_level: str
    target_role: str
    readiness_score: float
    current_streak: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- PROFILE SCHEMAS ---
class CandidateProfileOut(BaseModel):
    id: int
    user_id: int
    headline: str
    summary: str
    contact_info: Dict[str, Any]
    skills: Dict[str, List[str]]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    certifications: List[Dict[str, Any]]
    updated_at: datetime

    class Config:
        from_attributes = True

class CandidateProfileUpdate(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None
    skills: Optional[Dict[str, List[str]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Dict[str, Any]]] = None


# --- RESUME & ATS SCHEMAS ---
class ResumeOut(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_size_bytes: int
    raw_text: str
    ats_score: float
    ats_breakdown: Dict[str, Any]
    red_flags: List[Dict[str, Any]]
    tailored_version: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class JDMatchRequest(BaseModel):
    job_title: str
    job_description: str

class JDMatchResponse(BaseModel):
    match_percentage: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    tailored_checklist: List[str]
    fit_summary: str
    rewritten_bullets: List[Dict[str, str]]


# --- STUDY PLAN SCHEMAS ---
class StudyPlanCreate(BaseModel):
    role_title: str
    hours_per_day: float = 2.0
    total_weeks: int = 4

class StudyTaskOut(BaseModel):
    id: int
    week_number: int
    day_number: int
    tier: str
    title: str
    description: str
    topic: str
    resource_type: str
    resource_url: str
    is_completed: bool

    class Config:
        from_attributes = True

class StudyPlanOut(BaseModel):
    id: int
    role_title: str
    total_weeks: int
    hours_per_day: float
    status: str
    progress_percentage: float
    tasks: List[StudyTaskOut]

    class Config:
        from_attributes = True

class TargetRoleOut(BaseModel):
    id: int
    role_key: str
    title: str
    category: str
    description: str
    required_skills: List[str]
    nice_to_have_skills: List[str]
    core_competencies: List[str]
    typical_interview_rounds: List[Dict[str, Any]]

    class Config:
        from_attributes = True

class SkillGapReportOut(BaseModel):
    role_title: str
    match_percentage: float
    strong_skills: List[str]
    partial_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    created_at: Optional[datetime] = None


# --- INTERVIEW SCHEMAS ---
class InterviewStartRequest(BaseModel):
    role_title: str = "Software Engineer"
    level: int = 2 # 1, 2, 3
    persona: str = "Technical Lead"
    mode: str = "text" # text, voice, timed_round
    round_type: str = "Technical"

class InterviewAnswerRequest(BaseModel):
    turn_id: int
    answer_text: str
    audio_duration_sec: Optional[float] = 0.0
    filler_word_count: Optional[int] = 0
    speaking_wpm: Optional[float] = 0.0

class FeedbackOut(BaseModel):
    id: int
    score_overall: float
    score_relevance: float
    score_star_structure: float
    score_technical_accuracy: float
    score_clarity: float
    score_confidence: float
    score_conciseness: float
    critique: str
    sample_ideal_answer: str
    detected_weak_points: List[str]

    class Config:
        from_attributes = True

class InterviewTurnOut(BaseModel):
    id: int
    turn_index: int
    question_text: str
    question_category: str
    user_answer: str
    speaking_wpm: float
    filler_word_count: int
    feedback: Optional[FeedbackOut] = None

    class Config:
        from_attributes = True

class InterviewSessionOut(BaseModel):
    id: int
    role_title: str
    mode: str
    persona: str
    round_type: str
    level: int
    status: str
    overall_score: float
    total_turns: int
    summary_feedback: str
    strengths: List[str]
    weaknesses: List[str]
    suggested_topics_to_improve: List[str]
    wpm_average: float
    filler_words_total: int
    created_at: datetime
    turns: List[InterviewTurnOut] = []

    class Config:
        from_attributes = True


# --- CODING SCHEMAS ---
class CodeRunRequest(BaseModel):
    problem_id: str
    language: str = "python"
    code: str

class TestCaseResult(BaseModel):
    input_str: str
    expected_output: str
    actual_output: str
    passed: bool
    error: Optional[str] = None

class CodeRunResponse(BaseModel):
    status: str
    passed_cases: int
    total_cases: int
    runtime_ms: float
    test_results: List[TestCaseResult]
    ai_feedback: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None

class CodingProblemOut(BaseModel):
    id: str
    title: str
    difficulty: str
    category: str
    description: str
    examples: List[Dict[str, Any]]
    constraints: List[str]
    starter_code: Dict[str, str]
    hints: List[str]
    optimal_complexity: str

class CodingSubmissionOut(BaseModel):
    id: int
    problem_id: str
    problem_title: str
    language: str
    status: str
    passed_cases: int
    total_cases: int
    runtime_ms: float
    time_complexity: Optional[str]
    space_complexity: Optional[str]
    ai_feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- QUESTION BANK SCHEMAS ---
class QuestionBankOut(BaseModel):
    id: int
    role_id: Optional[int]
    role_title: Optional[str] = None
    level: int
    category: str
    question_text: str
    difficulty: str
    expected_keywords: List[str]
    ideal_star_answer: str
    rubric_hints: List[str]

    class Config:
        from_attributes = True

class QuestionListResponse(BaseModel):
    total: int
    questions: List[QuestionBankOut]
    categories: List[str]
    difficulties: List[str]


# --- GAMIFICATION & CAREER PACK SCHEMAS ---
class BadgeOut(BaseModel):
    id: int
    badge_key: str
    title: str
    description: str
    icon: str
    tier: str
    earned_at: datetime

    class Config:
        from_attributes = True

class DashboardStatsOut(BaseModel):
    readiness_score: float
    ats_score: float
    mock_avg_score: float
    solved_problems: int
    current_streak: int
    study_plan_progress: float
    badges: List[BadgeOut]
    recent_interviews: List[InterviewSessionOut]
    score_trend: List[Dict[str, Any]]
    skill_breakdown: List[Dict[str, Any]]
    weak_topics: List[Dict[str, Any]]

class CompanyPrepRequest(BaseModel):
    company_name: str
    role_title: str

class CompanyPrepOut(BaseModel):
    company_name: str
    role_title: str
    interview_rounds: List[Dict[str, Any]]
    common_questions: List[Dict[str, str]]
    culture_values_talking_points: List[str]
    questions_to_ask_interviewer: List[str]
    confidence_level: str

class CoverLetterRequest(BaseModel):
    company_name: str
    role_title: str
    job_description: Optional[str] = ""
    tone: Optional[str] = "Professional and confident"

class CoverLetterOut(BaseModel):
    cover_letter_text: str
    linkedin_summary: str
    thank_you_email_template: str
