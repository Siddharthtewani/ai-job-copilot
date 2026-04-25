from typing import Any

from sqlalchemy.orm import Session

from app.db.repositories.profile_repository import get_active_user_profile
from app.models.domain_models import MatchResult, ParsedJD
from app.services.retrieval_service import retrieve_top_evidence_for_jd


DISPLAY_NORMALIZATION = {
    "sql": "SQL",
    "aws": "AWS",
    "nlp": "NLP",
    "llms": "LLMs",
    "mlops": "MLOps",
    "power bi": "Power BI",
    "fastapi": "FastAPI",
    "scikit-learn": "Scikit-learn",
}


def _normalize_term(term: str) -> str:
    return term.strip().lower()


def _display_term(term: str) -> str:
    key = term.strip().lower()
    return DISPLAY_NORMALIZATION.get(key, term)


def _normalized_set(values: list[str]) -> set[str]:
    return {_normalize_term(v) for v in values if v and v.strip()}


def _sorted_display(values: set[str]) -> list[str]:
    return [_display_term(v) for v in sorted(values)]


def _ratio(matched_count: int, total_count: int) -> float:
    if total_count == 0:
        return 1.0
    return matched_count / total_count


def calculate_match_score(
    db: Session,
    parsed_jd: ParsedJD,
    evidence_limit: int = 5,
) -> dict[str, Any]:
    profile = get_active_user_profile(db)
    if not profile:
        raise ValueError("No active user profile found. Seed a canonical profile first.")

    retrieval_result = retrieve_top_evidence_for_jd(
        db=db,
        parsed_jd=parsed_jd,
        limit=evidence_limit,
    )

    top_evidence = retrieval_result["top_evidence"]

    jd_skill_set = _normalized_set(
        parsed_jd.required_skills + parsed_jd.preferred_skills
    )
    jd_tool_set = _normalized_set(parsed_jd.required_tools)

    profile_skill_set = _normalized_set(profile.skills or [])
    profile_tool_set = _normalized_set(profile.tools or [])

    evidence_term_set: set[str] = set()
    for item in top_evidence:
        evidence_term_set.update(_normalize_term(t) for t in item.matched_terms)

    matched_skills = jd_skill_set.intersection(profile_skill_set.union(evidence_term_set))
    matched_tools = jd_tool_set.intersection(profile_tool_set.union(evidence_term_set))

    missing_skills = jd_skill_set - matched_skills
    missing_tools = jd_tool_set - matched_tools

    skill_match_ratio = _ratio(len(matched_skills), len(jd_skill_set))
    tool_match_ratio = _ratio(len(matched_tools), len(jd_tool_set))

    total_required_terms = len(jd_skill_set.union(jd_tool_set))
    covered_required_terms = len((jd_skill_set.union(jd_tool_set)).intersection(evidence_term_set))
    evidence_coverage_ratio = _ratio(covered_required_terms, total_required_terms)

    overall_score = round(
        (skill_match_ratio * 50)
        + (tool_match_ratio * 30)
        + (evidence_coverage_ratio * 20),
        2,
    )

    match_result = MatchResult(
        overall_score=overall_score,
        matched_skills=_sorted_display(matched_skills),
        matched_tools=_sorted_display(matched_tools),
        missing_skills=_sorted_display(missing_skills),
        missing_tools=_sorted_display(missing_tools),
        evidence_count=len(top_evidence),
    )

    return {
        "profile_id": profile.id,
        "profile_name": profile.full_name,
        "match_result": match_result,
        "top_evidence": top_evidence,
        "score_breakdown": {
            "skill_match_ratio": round(skill_match_ratio, 3),
            "tool_match_ratio": round(tool_match_ratio, 3),
            "evidence_coverage_ratio": round(evidence_coverage_ratio, 3),
            "weights": {
                "skills": 50,
                "tools": 30,
                "evidence": 20,
            },
        },
    }