from app.db.session import SessionLocal
from app.models.domain_models import ParsedJD
from app.services.match_service import calculate_match_score


def main() -> None:
    db = SessionLocal()
    try:
        parsed_jd = ParsedJD(
            role_title="Data Scientist",
            required_skills=["Python", "SQL", "Machine Learning"],
            preferred_skills=["NLP"],
            required_tools=["FastAPI", "AWS"],
            keywords_for_ats=[
                "Python",
                "SQL",
                "Machine Learning",
                "NLP",
                "FastAPI",
                "AWS",
            ],
        )

        result = calculate_match_score(
            db=db,
            parsed_jd=parsed_jd,
            evidence_limit=5,
        )

        match = result["match_result"]

        print(f"Profile: {result['profile_name']}")
        print(f"Overall Score: {match.overall_score}")
        print(f"Matched Skills: {match.matched_skills}")
        print(f"Matched Tools: {match.matched_tools}")
        print(f"Missing Skills: {match.missing_skills}")
        print(f"Missing Tools: {match.missing_tools}")
        print(f"Evidence Count: {match.evidence_count}")
        print("\nScore Breakdown:")
        print(result["score_breakdown"])

        print("\nTop Evidence:\n")
        for item in result["top_evidence"]:
            print(f"- [{item.section}] {item.title} | score={item.score}")
            print(f"  matched_terms={item.matched_terms}")
            print(f"  {item.bullet_text}")
            print()

    finally:
        db.close()


if __name__ == "__main__":
    main()