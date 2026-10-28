import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    User, TargetRole, CandidateProfile, SkillGapReport, StudyPlan, StudyTask, Badge
)
from app.schemas import (
    TargetRoleOut, SkillGapReportOut, StudyPlanCreate, StudyPlanOut, StudyTaskOut
)
from app.services.auth import get_current_user
from app.services.llm_service import llm_service

router = APIRouter(prefix="", tags=["Study Plans & Roles"])

@router.get("/roles", response_model=List[TargetRoleOut])
def list_target_roles(db: Session = Depends(get_db)):
    """List all supported target job roles and their competency profiles"""
    roles = db.query(TargetRole).all()
    return roles

@router.get("/roles/{role_key}", response_model=TargetRoleOut)
def get_target_role(role_key: str, db: Session = Depends(get_db)):
    """Retrieve detailed role requirements by role key"""
    role = db.query(TargetRole).filter(TargetRole.role_key == role_key).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target role '{role_key}' not found."
        )
    return role

@router.get("/gap-report", response_model=SkillGapReportOut)
def get_skill_gap_report(
    role_key: Optional[str] = Query(None, description="Target role key, e.g. software_engineer"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze candidate skills against target role requirements and produce gap analysis"""
    # 1. Resolve role
    target_role = None
    if role_key:
        target_role = db.query(TargetRole).filter(TargetRole.role_key == role_key).first()
    if not target_role:
        # Match by user.target_role or default to software_engineer
        target_role = (
            db.query(TargetRole).filter(TargetRole.title.ilike(f"%{current_user.target_role}%")).first()
            or db.query(TargetRole).first()
        )
    
    if not target_role:
        raise HTTPException(status_code=404, detail="No target roles available in system.")

    # 2. Extract user's candidate profile skills
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    user_skill_set = set()
    if profile and profile.skills:
        for cat, skills in profile.skills.items():
            if isinstance(skills, list):
                for s in skills:
                    user_skill_set.add(s.lower().strip())

    # If no parsed skills yet, add baseline based on experience level
    if not user_skill_set:
        user_skill_set = {"python", "javascript", "git", "rest apis", "sql"}

    # 3. Classify role required skills
    required = target_role.required_skills or []
    nice_to_have = target_role.nice_to_have_skills or []

    strong = []
    partial = []
    missing = []

    # Common related tech associations for partial credit
    related_map = {
        "react": ["next.js", "vue", "javascript", "typescript"],
        "node.js": ["express", "javascript", "typescript", "backend"],
        "python": ["fastapi", "django", "flask"],
        "fastapi": ["python", "flask", "django"],
        "docker": ["kubernetes", "containers", "ci/cd"],
        "sql": ["postgresql", "mysql", "sqlite", "relational databases"],
        "postgresql": ["sql", "mysql", "relational databases"],
        "aws": ["cloud", "gcp", "azure"],
        "ci/cd": ["git", "github actions", "docker"]
    }

    for req in required:
        req_norm = req.lower().strip()
        if req_norm in user_skill_set:
            strong.append(req)
        else:
            # Check related map
            related_tokens = related_map.get(req_norm, [])
            if any(rel in user_skill_set for rel in related_tokens) or any(req_norm in s for s in user_skill_set):
                partial.append(req)
            else:
                missing.append(req)

    # Add some nice-to-haves into partial / missing
    for nth in nice_to_have[:3]:
        nth_norm = nth.lower().strip()
        if nth_norm in user_skill_set:
            if nth not in strong:
                strong.append(nth)
        elif nth not in partial and nth not in missing:
            missing.append(nth)

    total_req_count = max(len(required), 1)
    match_percentage = min(100.0, max(15.0, round(((len(strong) * 1.0 + len(partial) * 0.5) / total_req_count) * 100, 1)))

    # Recommendations
    recommendations = []
    if missing:
        recommendations.append(f"Priority focus: Master missing core competencies: {', '.join(missing[:3])}.")
    if partial:
        recommendations.append(f"Reinforce partial knowledge in {', '.join(partial[:2])} by completing hands-on architectural projects.")
    recommendations.append(f"Structure your interview STAR stories to emphasize technical depth in {strong[0] if strong else 'core engineering fundamentals'}.")

    # Save or update report in DB
    gap_record = SkillGapReport(
        user_id=current_user.id,
        role_title=target_role.title,
        match_percentage=match_percentage,
        strong_skills=strong,
        partial_skills=partial,
        missing_skills=missing,
        recommendations=recommendations,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(gap_record)
    db.commit()

    return SkillGapReportOut(
        role_title=target_role.title,
        match_percentage=match_percentage,
        strong_skills=strong,
        partial_skills=partial,
        missing_skills=missing,
        recommendations=recommendations,
        created_at=gap_record.created_at
    )


def _build_default_tasks(role_title: str, plan_id: int) -> List[StudyTask]:
    """Curated, high-yield multi-week tasks across BASIC, INTERMEDIATE, and ADVANCED tiers"""
    tasks_data = [
        # Week 1: Foundations & Core Architecture (BASIC)
        {
            "week_number": 1, "day_number": 1, "tier": "BASIC",
            "title": f"Review Core {role_title} Foundations & Language Internals",
            "description": "Deep-dive into memory models, call stacks, event loops, and asynchronous runtime primitives.",
            "topic": "Fundamentals", "resource_type": "article",
            "resource_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop"
        },
        {
            "week_number": 1, "day_number": 2, "tier": "BASIC",
            "title": "Master Clean RESTful API Design & Status Code Standards",
            "description": "Understand idempotency, pagination, error payloads, and HTTP caching headers (ETag, Cache-Control).",
            "topic": "API Design", "resource_type": "documentation",
            "resource_url": "https://restfulapi.net/"
        },
        {
            "week_number": 1, "day_number": 3, "tier": "BASIC",
            "title": "SQL Indexing, B-Trees & Relational Query Optimization",
            "description": "Analyze EXPLAIN ANALYZE execution plans, compound indexes, and N+1 query avoidance.",
            "topic": "Databases", "resource_type": "article",
            "resource_url": "https://use-the-index-luke.com/"
        },
        {
            "week_number": 1, "day_number": 4, "tier": "BASIC",
            "title": "Data Structures Sprint: HashMaps, Heaps & Two Pointers",
            "description": "Solve 3 foundational interview problems emphasizing space/time complexity trade-offs.",
            "topic": "Algorithms", "resource_type": "practice",
            "resource_url": "https://leetcode.com/explore/featured/card/top-interview-questions-easy/"
        },
        {
            "week_number": 1, "day_number": 5, "tier": "BASIC",
            "title": "Behavioral Foundations: Crafting 4 Core STAR Stories",
            "description": "Structure Situation, Task, Action, and Result for conflict resolution and technical failures.",
            "topic": "Behavioral", "resource_type": "practice",
            "resource_url": "https://www.themuse.com/advice/star-interview-method"
        },

        # Week 2: Intermediate Distributed Concepts & State Management (INTERMEDIATE)
        {
            "week_number": 2, "day_number": 1, "tier": "INTERMEDIATE",
            "title": "Caching Architecture: Redis Invalidation & Write Strategies",
            "description": "Compare Cache-Aside, Write-Through, and Write-Behind. Address cache stampedes and thundering herds.",
            "topic": "System Design", "resource_type": "article",
            "resource_url": "https://redis.io/resources/"
        },
        {
            "week_number": 2, "day_number": 2, "tier": "INTERMEDIATE",
            "title": "Authentication Deep Dive: JWT, OAuth2 & Session Revocation",
            "description": "Implement secure refresh token rotation, CSRF protection, and HttpOnly cookies.",
            "topic": "Security", "resource_type": "documentation",
            "resource_url": "https://auth0.com/intro-to-iam/what-is-oauth-2"
        },
        {
            "week_number": 2, "day_number": 3, "tier": "INTERMEDIATE",
            "title": "Containerization & Docker Multi-Stage Optimization",
            "description": "Construct minimal production Docker images with non-root security principles and Alpine bases.",
            "topic": "DevOps", "resource_type": "documentation",
            "resource_url": "https://docs.docker.com/develop/develop-images/multistage-build/"
        },
        {
            "week_number": 2, "day_number": 4, "tier": "INTERMEDIATE",
            "title": "Trees, Graphs & BFS/DFS Traversal Mastery",
            "description": "Solve connected components, topological sorting, and shortest path interview challenges.",
            "topic": "Algorithms", "resource_type": "practice",
            "resource_url": "https://leetcode.com/tag/depth-first-search/"
        },
        {
            "week_number": 2, "day_number": 5, "tier": "INTERMEDIATE",
            "title": "Technical Deep Dive: Explaining Architecture Trade-offs",
            "description": "Practice verbalizing technical choices: Monolith vs Microservices, SQL vs NoSQL, Sync vs Async.",
            "topic": "Communication", "resource_type": "practice",
            "resource_url": "https://highscalability.com/"
        },

        # Week 3: Scalability, Concurrency & High Availability (ADVANCED)
        {
            "week_number": 3, "day_number": 1, "tier": "ADVANCED",
            "title": "Distributed Messaging: Kafka vs RabbitMQ Event Streaming",
            "description": "Partitioning, consumer groups, exactly-once semantics, and dead letter queue architectures.",
            "topic": "System Design", "resource_type": "article",
            "resource_url": "https://kafka.apache.org/documentation/"
        },
        {
            "week_number": 3, "day_number": 2, "tier": "ADVANCED",
            "title": "Database Scaling: Sharding, Read Replicas & CAP Theorem",
            "description": "Consistent hashing, replication lag mitigation, and strong vs eventual consistency paradigms.",
            "topic": "Databases", "resource_type": "article",
            "resource_url": "https://en.wikipedia.org/wiki/CAP_theorem"
        },
        {
            "week_number": 3, "day_number": 3, "tier": "ADVANCED",
            "title": "Rate Limiting & Resiliency Patterns (Circuit Breakers)",
            "description": "Implement token bucket and sliding window rate limiters in distributed systems.",
            "topic": "System Design", "resource_type": "article",
            "resource_url": "https://martinfowler.com/bliki/CircuitBreaker.html"
        },
        {
            "week_number": 3, "day_number": 4, "tier": "ADVANCED",
            "title": "Dynamic Programming & Complex Optimization Challenges",
            "description": "Identify overlapping subproblems and optimal substructure; master memoization vs tabulation.",
            "topic": "Algorithms", "resource_type": "practice",
            "resource_url": "https://leetcode.com/tag/dynamic-programming/"
        },
        {
            "week_number": 3, "day_number": 5, "tier": "ADVANCED",
            "title": "Mock Interview Session: High-Scale System Design",
            "description": "Complete a full 45-minute simulation designing a URL Shortener or Global Chat Service.",
            "topic": "Mock Interview", "resource_type": "practice",
            "resource_url": "https://github.com/donnemartin/system-design-primer"
        },

        # Week 4: Capstone Execution & Full-Round Readiness (ADVANCED)
        {
            "week_number": 4, "day_number": 1, "tier": "ADVANCED",
            "title": "End-to-End System Observability: OpenTelemetry & Metrics",
            "description": "Trace distributed requests across microservices and analyze p95/p99 latency spikes.",
            "topic": "Observability", "resource_type": "documentation",
            "resource_url": "https://opentelemetry.io/"
        },
        {
            "week_number": 4, "day_number": 2, "tier": "ADVANCED",
            "title": "STAR Behavioral Polish: Executive Presence & Leadership",
            "description": "Practice answering: 'Tell me about a time you disagreed with leadership and influenced the outcome.'",
            "topic": "Behavioral", "resource_type": "practice",
            "resource_url": "https://hbr.org/2021/04/how-to-tell-a-great-story-in-a-job-interview"
        },
        {
            "week_number": 4, "day_number": 3, "tier": "ADVANCED",
            "title": "Live Mock Interview: Full Technical & Behavioral Round",
            "description": "Simulate back-to-back coding and conceptual rounds with strict grading criteria.",
            "topic": "Mock Interview", "resource_type": "practice",
            "resource_url": "http://localhost:5173"
        },
        {
            "week_number": 4, "day_number": 4, "tier": "ADVANCED",
            "title": "Questions for Interviewers: Assessing Culture & Architecture",
            "description": "Prepare 6 reverse-interview questions that demonstrate strategic engineering acumen.",
            "topic": "Interview Prep", "resource_type": "article",
            "resource_url": "https://github.com/viraptor/reverse-interview"
        },
        {
            "week_number": 4, "day_number": 5, "tier": "ADVANCED",
            "title": "Final Readiness Checklist & Portfolio Deployment",
            "description": "Finalize your GitHub READMEs, ensure live demos are operational, and verify your ATS resume score >= 85%.",
            "topic": "Career Launch", "resource_type": "practice",
            "resource_url": "http://localhost:5173"
        }
    ]

    task_objects = []
    for t in tasks_data:
        obj = StudyTask(
            plan_id=plan_id,
            week_number=t["week_number"],
            day_number=t["day_number"],
            tier=t["tier"],
            title=t["title"],
            description=t["description"],
            topic=t["topic"],
            resource_type=t["resource_type"],
            resource_url=t["resource_url"],
            is_completed=False
        )
        task_objects.append(obj)
    return task_objects


@router.post("/plans/generate", response_model=StudyPlanOut)
def generate_study_plan(
    plan_data: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate or regenerate a customized 4-week structured preparation syllabus"""
    # Archive previous active plans
    existing_plans = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id,
        StudyPlan.status == "active"
    ).all()
    for p in existing_plans:
        p.status = "archived"

    # Create new study plan
    new_plan = StudyPlan(
        user_id=current_user.id,
        role_title=plan_data.role_title,
        total_weeks=plan_data.total_weeks,
        hours_per_day=plan_data.hours_per_day,
        status="active",
        progress_percentage=0.0,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    # Populate tasks
    tasks = _build_default_tasks(plan_data.role_title, new_plan.id)
    db.add_all(tasks)
    db.commit()
    db.refresh(new_plan)

    return new_plan


@router.get("/plans/current", response_model=StudyPlanOut)
def get_current_study_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch active study plan, auto-generating one if not yet initialized"""
    plan = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id,
        StudyPlan.status == "active"
    ).order_by(StudyPlan.id.desc()).first()

    if not plan:
        # Generate initial plan
        role_title = current_user.target_role or "Software Engineer"
        new_plan = StudyPlan(
            user_id=current_user.id,
            role_title=role_title,
            total_weeks=4,
            hours_per_day=2.0,
            status="active",
            progress_percentage=0.0,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        tasks = _build_default_tasks(role_title, new_plan.id)
        db.add_all(tasks)
        db.commit()
        db.refresh(new_plan)
        return new_plan

    return plan


@router.patch("/plans/tasks/{task_id}/toggle", response_model=StudyPlanOut)
def toggle_study_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle a task's completion status, updating syllabus progress and user readiness score"""
    task = db.query(StudyTask).join(StudyPlan).filter(
        StudyTask.id == task_id,
        StudyPlan.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized.")

    task.is_completed = not task.is_completed
    task.completed_at = datetime.datetime.now(datetime.timezone.utc) if task.is_completed else None

    # Recalculate plan progress
    plan = db.query(StudyPlan).filter(StudyPlan.id == task.plan_id).first()
    all_tasks = plan.tasks
    completed_count = sum(1 for t in all_tasks if t.is_completed)
    total_count = len(all_tasks)
    plan.progress_percentage = round((completed_count / max(total_count, 1)) * 100, 1)

    # Award readiness score points & check badges
    delta_score = 1.5 if task.is_completed else -1.5
    current_user.readiness_score = min(100.0, max(0.0, round(current_user.readiness_score + delta_score, 1)))

    if completed_count >= 5:
        # Check for study streak badge
        badge = db.query(Badge).filter(Badge.user_id == current_user.id, Badge.badge_key == "study_sprinter").first()
        if not badge:
            b = Badge(
                user_id=current_user.id,
                badge_key="study_sprinter",
                title="Syllabus Sprinter",
                description="Completed 5 roadmap curriculum milestones in PrepPilot.",
                icon="zap",
                tier="Bronze"
            )
            db.add(b)

    db.commit()
    db.refresh(plan)
    return plan
