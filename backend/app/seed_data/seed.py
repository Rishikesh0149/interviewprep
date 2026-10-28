import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, engine, Base
from app.models import TargetRole, QuestionBank
from app.seed_data.roles_knowledge_base import ROLES_DATA
from app.seed_data.question_bank import generate_seed_questions

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("[*] Checking Target Roles...")
        role_map = {}
        for r in ROLES_DATA:
            existing = db.query(TargetRole).filter(TargetRole.role_key == r["role_key"]).first()
            if not existing:
                role_obj = TargetRole(
                    role_key=r["role_key"],
                    title=r["title"],
                    category=r["category"],
                    description=r["description"],
                    required_skills=r["required_skills"],
                    nice_to_have_skills=r["nice_to_have_skills"],
                    core_competencies=r["core_competencies"],
                    typical_interview_rounds=r["typical_interview_rounds"]
                )
                db.add(role_obj)
                db.commit()
                db.refresh(role_obj)
                role_map[r["role_key"]] = role_obj.id
                print(f" [+] Inserted role: {r['title']}")
            else:
                role_map[r["role_key"]] = existing.id

        print(f"[*] Total Roles in DB: {db.query(TargetRole).count()}")

        print("[*] Checking Question Bank...")
        all_questions = generate_seed_questions()
        inserted_count = 0

        for q in all_questions:
            existing = db.query(QuestionBank).filter(QuestionBank.question_text == q["question_text"]).first()
            if not existing:
                role_id = role_map.get(q["role_key"]) if q["role_key"] else None
                q_obj = QuestionBank(
                    role_id=role_id,
                    level=q["level"],
                    category=q["category"],
                    question_text=q["question_text"],
                    difficulty=q["difficulty"],
                    expected_keywords=q["expected_keywords"],
                    ideal_star_answer=q["ideal_star_answer"],
                    rubric_hints=q["rubric_hints"]
                )
                db.add(q_obj)
                inserted_count += 1

        db.commit()
        total_questions = db.query(QuestionBank).count()
        print(f" [+] Inserted {inserted_count} new questions. Total in Bank: {total_questions}")

    except Exception as e:
        db.rollback()
        print(f" [!] Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
