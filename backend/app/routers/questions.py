from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import QuestionBank, TargetRole
from app.schemas import QuestionBankOut, QuestionListResponse

router = APIRouter(prefix="/questions", tags=["Question Bank"])

CATEGORIES = ["Technical", "Behavioral", "System Design", "HR", "Coding"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

@router.get("", response_model=QuestionListResponse)
def list_questions(
    role_id: Optional[int] = Query(None, description="Filter by TargetRole ID"),
    category: Optional[str] = Query(None, description="Filter by Category"),
    difficulty: Optional[str] = Query(None, description="Filter by Difficulty"),
    level: Optional[int] = Query(None, description="Filter by Level (1, 2, 3)"),
    search: Optional[str] = Query(None, description="Keyword search in question or answer"),
    skip: int = Query(0, ge=0),
    limit: int = Query(40, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search and browse curated questions with ideal STAR answers and rubric hints"""
    query = db.query(QuestionBank)

    if role_id is not None:
        query = query.filter(QuestionBank.role_id == role_id)
    if category:
        query = query.filter(QuestionBank.category.ilike(category))
    if difficulty:
        query = query.filter(QuestionBank.difficulty.ilike(difficulty))
    if level is not None:
        query = query.filter(QuestionBank.level == level)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                QuestionBank.question_text.ilike(search_pattern),
                QuestionBank.ideal_star_answer.ilike(search_pattern)
            )
        )

    total_count = query.count()
    raw_questions = query.offset(skip).limit(limit).all()

    # Pre-fetch roles map for fast role title lookup
    role_map = {r.id: r.title for r in db.query(TargetRole).all()}

    questions_out = []
    for q in raw_questions:
        item = QuestionBankOut(
            id=q.id,
            role_id=q.role_id,
            role_title=role_map.get(q.role_id, "General"),
            level=q.level,
            category=q.category,
            question_text=q.question_text,
            difficulty=q.difficulty,
            expected_keywords=q.expected_keywords or [],
            ideal_star_answer=q.ideal_star_answer or "",
            rubric_hints=q.rubric_hints or []
        )
        questions_out.append(item)

    return QuestionListResponse(
        total=total_count,
        questions=questions_out,
        categories=CATEGORIES,
        difficulties=DIFFICULTIES
    )


@router.get("/{question_id}", response_model=QuestionBankOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Retrieve full details of a single interview question"""
    q = db.query(QuestionBank).filter(QuestionBank.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found in repository.")

    role_title = "General"
    if q.role_id:
        role = db.query(TargetRole).filter(TargetRole.id == q.role_id).first()
        if role:
            role_title = role.title

    return QuestionBankOut(
        id=q.id,
        role_id=q.role_id,
        role_title=role_title,
        level=q.level,
        category=q.category,
        question_text=q.question_text,
        difficulty=q.difficulty,
        expected_keywords=q.expected_keywords or [],
        ideal_star_answer=q.ideal_star_answer or "",
        rubric_hints=q.rubric_hints or []
    )
