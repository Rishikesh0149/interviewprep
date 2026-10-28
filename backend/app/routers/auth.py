from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.models import User, CandidateProfile, Badge, ProgressSnapshot
from app.schemas import UserCreate, UserLogin, UserOut, Token
from app.services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        experience_level=user_in.experience_level or "intermediate",
        target_role=user_in.target_role or "Software Engineer",
        readiness_score=15.0,
        current_streak=1,
        last_active_date=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize empty candidate profile
    profile = CandidateProfile(
        user_id=user.id,
        headline=f"{user.experience_level.capitalize()} {user.target_role}",
        summary="",
        contact_info={"email": user.email, "name": user.full_name},
        skills={"languages": [], "frameworks": [], "databases": [], "tools": [], "soft_skills": []},
        experience=[],
        education=[],
        projects=[],
        certifications=[]
    )
    db.add(profile)

    # Award Welcome Badge
    welcome_badge = Badge(
        user_id=user.id,
        badge_key="first_step",
        title="PrepPilot Trainee",
        description="Created an account and started your interview readiness journey.",
        icon="rocket",
        tier="Bronze"
    )
    db.add(welcome_badge)

    # Create initial progress snapshot
    snapshot = ProgressSnapshot(
        user_id=user.id,
        readiness_score=15.0,
        ats_score=0.0,
        interview_avg_score=0.0,
        coding_problems_solved=0,
        streak_days=1,
    )
    db.add(snapshot)
    db.commit()

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "experience_level": user.experience_level,
            "target_role": user.target_role,
            "readiness_score": user.readiness_score,
            "current_streak": user.current_streak,
            "created_at": user.created_at.isoformat()
        },
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    }

@router.post("/login", response_model=dict)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    # Update streak if active on a new day
    today = datetime.utcnow().date()
    last_active = user.last_active_date.date() if user.last_active_date else today
    if (today - last_active).days == 1:
        user.current_streak += 1
    elif (today - last_active).days > 1:
        user.current_streak = 1
    user.last_active_date = datetime.utcnow()
    db.commit()

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "experience_level": user.experience_level,
            "target_role": user.target_role,
            "readiness_score": user.readiness_score,
            "current_streak": user.current_streak,
            "created_at": user.created_at.isoformat()
        },
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    }

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/refresh", response_model=dict)
def refresh_token(refresh_token_str: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token_str, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(user.id)
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.delete("/account", status_code=status.HTTP_200_OK)
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """One-click delete all user data (privacy & security compliance)"""
    db.delete(current_user)
    db.commit()
    return {"message": "All user data, resumes, interviews, and progress have been permanently deleted."}
