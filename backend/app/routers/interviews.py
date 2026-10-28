import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import (
    User, TargetRole, QuestionBank, InterviewSession, InterviewTurn, Feedback, ProgressSnapshot, Badge
)
from app.schemas import (
    InterviewStartRequest, InterviewAnswerRequest, InterviewSessionOut, InterviewTurnOut, FeedbackOut
)
from app.services.auth import get_current_user
from app.services.llm_service import llm_service

router = APIRouter(prefix="/interviews", tags=["Mock Interview Simulator"])

MAX_TURNS_PER_SESSION = 4

@router.post("/start", response_model=InterviewSessionOut)
def start_interview_session(
    payload: InterviewStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start an interactive mock interview simulation with adaptive persona and level"""
    # 1. Resolve questions for this role and round
    role = db.query(TargetRole).filter(TargetRole.title.ilike(f"%{payload.role_title}%")).first()
    role_id = role.id if role else None

    # Fetch question pool
    q_query = db.query(QuestionBank)
    if payload.round_type.lower() in ["behavioral", "hr"]:
        q_query = q_query.filter(QuestionBank.category.in_(["Behavioral", "HR"]))
    elif payload.round_type.lower() in ["system design"]:
        q_query = q_query.filter(QuestionBank.category == "System Design")
    else:
        # Technical
        q_query = q_query.filter(QuestionBank.category.in_(["Technical", "Coding"]))

    if role_id:
        role_questions = q_query.filter(QuestionBank.role_id == role_id).all()
        if not role_questions:
            questions = q_query.filter(QuestionBank.level == payload.level).all()
        else:
            questions = role_questions
    else:
        questions = q_query.filter(QuestionBank.level == payload.level).all()

    if not questions:
        questions = db.query(QuestionBank).all()

    first_q = questions[0] if questions else None
    first_q_text = (
        first_q.question_text if first_q 
        else f"Can you walk me through your engineering background and how you design scalable systems as a {payload.role_title}?"
    )
    first_q_cat = first_q.category if first_q else payload.round_type

    # 2. Create InterviewSession
    session = InterviewSession(
        user_id=current_user.id,
        role_title=payload.role_title,
        mode=payload.mode,
        persona=payload.persona,
        round_type=payload.round_type,
        level=payload.level,
        status="in_progress",
        overall_score=0.0,
        total_turns=1,
        summary_feedback="",
        strengths=[],
        weaknesses=[],
        suggested_topics_to_improve=[],
        wpm_average=0.0,
        filler_words_total=0,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # 3. Create initial turn
    first_turn = InterviewTurn(
        session_id=session.id,
        turn_index=1,
        question_text=first_q_text,
        question_category=first_q_cat,
        user_answer="",
        speaking_wpm=0.0,
        filler_word_count=0,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(first_turn)
    db.commit()
    db.refresh(session)

    return session


@router.post("/turn/answer", response_model=InterviewSessionOut)
def submit_turn_answer(
    payload: InterviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit candidate's answer for STAR evaluation, scoring, and trigger the next dynamic question"""
    turn = db.query(InterviewTurn).filter(InterviewTurn.id == payload.turn_id).first()
    if not turn:
        raise HTTPException(status_code=404, detail="Interview turn not found.")

    session = db.query(InterviewSession).filter(
        InterviewSession.id == turn.session_id,
        InterviewSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=403, detail="Unauthorized access to interview session.")

    # Update turn metrics
    turn.user_answer = payload.answer_text.strip()
    turn.audio_duration_sec = payload.audio_duration_sec or 0.0
    turn.filler_word_count = payload.filler_word_count or 0
    turn.speaking_wpm = payload.speaking_wpm or 0.0

    # Evaluate answer using LLM
    eval_system_prompt = (
        f"You are an expert technical interviewer evaluating a {session.role_title} candidate (Level {session.level}) "
        f"adopting the persona of '{session.persona}'. Evaluate the candidate's answer using the STAR method and deep technical metrics.\n"
        "Return a JSON object with EXACTLY the following structure:\n"
        "{\n"
        '  "score_overall": 8.0,\n'
        '  "score_relevance": 8.5,\n'
        '  "score_star_structure": 7.5,\n'
        '  "score_technical_accuracy": 8.0,\n'
        '  "score_clarity": 8.0,\n'
        '  "score_confidence": 7.5,\n'
        '  "score_conciseness": 8.0,\n'
        '  "critique": "Constructive 2-3 sentence critique highlighting what was strong and specific ways to elevate to senior caliber.",\n'
        '  "sample_ideal_answer": "A compelling 3-4 sentence senior exemplar answer displaying quantified outcomes.",\n'
        '  "detected_weak_points": ["Specific technical gap 1", "Specific delivery gap 2"]\n'
        "}"
    )

    eval_user_prompt = (
        f"Question: {turn.question_text}\n"
        f"Category: {turn.question_category}\n"
        f"Candidate Answer: {turn.user_answer if turn.user_answer else '[Candidate did not provide a response]'}\n"
        f"Audio duration: {turn.audio_duration_sec}s, Speaking WPM: {turn.speaking_wpm}, Filler words: {turn.filler_word_count}"
    )

    eval_json = llm_service.generate_json_response(eval_system_prompt, eval_user_prompt)

    # Save Feedback record
    feedback = Feedback(
        turn_id=turn.id,
        score_overall=float(eval_json.get("score_overall", 7.5)),
        score_relevance=float(eval_json.get("score_relevance", 7.5)),
        score_star_structure=float(eval_json.get("score_star_structure", 7.0)),
        score_technical_accuracy=float(eval_json.get("score_technical_accuracy", 7.5)),
        score_clarity=float(eval_json.get("score_clarity", 7.5)),
        score_confidence=float(eval_json.get("score_confidence", 7.5)),
        score_conciseness=float(eval_json.get("score_conciseness", 7.5)),
        critique=eval_json.get("critique", "Good foundational structure. To elevate your answer, quantify business outcomes and highlight architectural tradeoffs."),
        sample_ideal_answer=eval_json.get("sample_ideal_answer", "In our production system handling high traffic, I designed and deployed an event-driven queue with dead-letter monitoring, reducing latency by 35%."),
        detected_weak_points=eval_json.get("detected_weak_points", ["Could include more specific latency or throughput figures."])
    )
    db.add(feedback)
    db.commit()

    # Determine if next question is needed
    existing_turns = db.query(InterviewTurn).filter(InterviewTurn.session_id == session.id).all()
    current_turn_count = len(existing_turns)

    if current_turn_count < MAX_TURNS_PER_SESSION and session.status == "in_progress":
        # Find next distinct question
        used_questions = {t.question_text for t in existing_turns}
        role = db.query(TargetRole).filter(TargetRole.title.ilike(f"%{session.role_title}%")).first()
        role_id = role.id if role else None

        candidates = db.query(QuestionBank)
        if session.round_type.lower() in ["behavioral", "hr"]:
            candidates = candidates.filter(QuestionBank.category.in_(["Behavioral", "HR"]))
        elif session.round_type.lower() in ["system design"]:
            candidates = candidates.filter(QuestionBank.category == "System Design")
        else:
            candidates = candidates.filter(QuestionBank.category.in_(["Technical", "Coding"]))

        if role_id:
            role_pool = candidates.filter(QuestionBank.role_id == role_id).all()
            if role_pool:
                candidates_list = [q for q in role_pool if q.question_text not in used_questions]
            else:
                candidates_list = [q for q in candidates.all() if q.question_text not in used_questions]
        else:
            candidates_list = [q for q in candidates.all() if q.question_text not in used_questions]

        if not candidates_list:
            all_pool = db.query(QuestionBank).all()
            candidates_list = [q for q in all_pool if q.question_text not in used_questions]

        if candidates_list:
            next_q = candidates_list[0]
            next_q_text = next_q.question_text
            next_q_cat = next_q.category
        else:
            next_q_text = f"Describe an instance where you optimized a bottleneck in a {session.role_title} project and explain how you measured success."
            next_q_cat = "Technical"

        next_turn = InterviewTurn(
            session_id=session.id,
            turn_index=current_turn_count + 1,
            question_text=next_q_text,
            question_category=next_q_cat,
            user_answer="",
            speaking_wpm=0.0,
            filler_word_count=0,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(next_turn)
        session.total_turns = current_turn_count + 1
        db.commit()

    db.refresh(session)
    return session


@router.post("/{session_id}/complete", response_model=InterviewSessionOut)
def complete_interview_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Finalize the mock interview, generate end-of-session debrief report, and update readiness score"""
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    turns = db.query(InterviewTurn).filter(InterviewTurn.session_id == session.id).all()
    feedback_scores = []
    all_weaknesses = []
    all_critiques = []
    total_wpm = 0.0
    total_fillers = 0
    turns_with_wpm = 0

    for t in turns:
        if t.feedback:
            feedback_scores.append(t.feedback.score_overall)
            all_critiques.append(t.feedback.critique)
            if t.feedback.detected_weak_points:
                all_weaknesses.extend(t.feedback.detected_weak_points)
        if t.speaking_wpm > 0:
            total_wpm += t.speaking_wpm
            turns_with_wpm += 1
        total_fillers += t.filler_word_count

    avg_score = round(sum(feedback_scores) / len(feedback_scores), 1) if feedback_scores else 7.5
    avg_wpm = round(total_wpm / max(turns_with_wpm, 1), 1)

    strengths = [
        "Structured technical explanations adhering to engineering fundamentals.",
        "Clear articulation of problem framing and conceptual boundaries."
    ]
    if avg_wpm >= 110 and avg_wpm <= 160:
        strengths.append(f"Ideal speaking cadence averaging {avg_wpm} words per minute.")

    weaknesses = list(dict.fromkeys(all_weaknesses))[:3]
    if not weaknesses:
        weaknesses = ["Incorporate more quantified metrics in the Result phase of STAR answers."]

    suggested_topics = [
        f"{session.role_title} System Architecture & Latency Budgets",
        "STAR Quantifiable Outcomes & Metrics Articulation",
        "Concurrency & Distributed Consistency Paradigms"
    ]

    summary = (
        f"You completed a Level {session.level} {session.round_type} interview simulation with the '{session.persona}' persona. "
        f"Your overall score was {avg_score}/10. {strengths[0]} {weaknesses[0]}"
    )

    session.status = "completed"
    session.overall_score = avg_score
    session.summary_feedback = summary
    session.strengths = strengths
    session.weaknesses = weaknesses
    session.suggested_topics_to_improve = suggested_topics
    session.wpm_average = avg_wpm
    session.filler_words_total = total_fillers
    session.completed_at = datetime.datetime.now(datetime.timezone.utc)

    # Update user readiness score
    score_boost = round((avg_score / 10.0) * 4.0, 1)
    current_user.readiness_score = min(100.0, max(0.0, round(current_user.readiness_score + score_boost, 1)))

    # Record snapshot
    snapshot = ProgressSnapshot(
        user_id=current_user.id,
        readiness_score=current_user.readiness_score,
        ats_score=current_user.resumes[0].ats_score if current_user.resumes else 75.0,
        interview_avg_score=avg_score,
        coding_problems_solved=len(current_user.coding_submissions),
        streak_days=current_user.current_streak,
        snapshot_date=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(snapshot)

    # Award Badges
    first_badge = db.query(Badge).filter(Badge.user_id == current_user.id, Badge.badge_key == "first_interview").first()
    if not first_badge:
        b1 = Badge(
            user_id=current_user.id,
            badge_key="first_interview",
            title="First Flight",
            description="Completed your first AI-simulated technical interview on PrepPilot.",
            icon="mic",
            tier="Bronze"
        )
        db.add(b1)

    if avg_score >= 8.5:
        ace_badge = db.query(Badge).filter(Badge.user_id == current_user.id, Badge.badge_key == "interview_ace").first()
        if not ace_badge:
            b2 = Badge(
                user_id=current_user.id,
                badge_key="interview_ace",
                title="Interview Ace",
                description="Achieved an 8.5+ rating on an adaptive technical interview round.",
                icon="award",
                tier="Silver"
            )
            db.add(b2)

    db.commit()
    db.refresh(session)
    return session


@router.get("/{session_id}", response_model=InterviewSessionOut)
def get_interview_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve full transcript and evaluation report of a specific interview session"""
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    return session


@router.get("", response_model=List[InterviewSessionOut])
def list_user_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List historical interview sessions completed by the candidate"""
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.id.desc()).all()
    return sessions
