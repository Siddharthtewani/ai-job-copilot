from app.db.session import SessionLocal
from app.models.domain_models import ParsedJD
from app.services.retrieval_service import retrieve_top_evidence_for_jd


def main() -> None:
    db = SessionLocal()
    try:
        parsed_jd = ParsedJD(
            role_title="Data Scientist",
            required_skills=["Python", "SQL", "Machine Learning"],
            required_tools=["FastAPI", "AWS"],
            keywords_for_ats=["Python", "SQL", "FastAPI", "AWS", "Machine Learning"],
        )

        result = retrieve_top_evidence_for_jd(
            db=db,
            parsed_jd=parsed_jd,
            limit=5,
        )

        print(f"Profile: {result['profile_name']}")
        print(f"Bullets considered: {result['total_bullets_considered']}")
        print("\nTop evidence:\n")

        for item in result["top_evidence"]:
            print(f"- [{item.section}] {item.title} | score={item.score}")
            print(f"  matched_terms={item.matched_terms}")
            print(f"  {item.bullet_text}")
            print()

    finally:
        db.close()


if __name__ == "__main__":
    main()