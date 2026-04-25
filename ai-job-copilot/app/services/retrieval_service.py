from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.db.repositories.profile_repository import (
    get_active_user_profile,
    get_resume_bullets_for_profile,
)
from app.models.domain_models import ParsedJD


DISPLAY_NORMALIZATION = {
    "sql": "SQL",
    "aws": "AWS",
    "nlp": "NLP",
    "llms": "LLMs",
    "mlops": "MLOps",
    "power bi": "Power BI",
    "fastapi": "FastAPI",
}


@dataclass
class RetrievedEvidence:
    bullet_id: int
    section: str
    title: str | None
    organization: str | None
    bullet_text: str
    matched_terms: list[str]
    score: int


def _normalize_term(term: str) -> str:
    return term.strip().lower()


def _display_term(term: str) -> str:
    key = term.strip().lower()
    return DISPLAY_NORMALIZATION.get(key, term)


def _unique_normalized(values: list[str]) -> set[str]:
    return {_normalize_term(v) for v in values if v and v.strip()}


def _score_bullet(
    bullet_text: str,
    bullet_skills: list[str],
    bullet_tools: list[str],
    bullet_tags: list[str],
    jd_terms: set[str],
) -> tuple[int, list[str]]:
    matched_terms = set()

    bullet_skill_set = _unique_normalized(bullet_skills)
    bullet_tool_set = _unique_normalized(bullet_tools)
    bullet_tag_set = _unique_normalized(bullet_tags)
    bullet_text_lower = bullet_text.lower()

    for term in jd_terms:
        if (
            term in bullet_skill_set
            or term in bullet_tool_set
            or term in bullet_tag_set
            or term in bullet_text_lower
        ):
            matched_terms.add(term)

    score = len(matched_terms)
    return score, [_display_term(t) for t in sorted(matched_terms)]


def retrieve_top_evidence_for_jd(
    db: Session,
    parsed_jd: ParsedJD,
    limit: int = 5,
) -> dict[str, Any]:
    profile = get_active_user_profile(db)
    if not profile:
        raise ValueError("No active user profile found. Seed a canonical profile first.")

    bullets = get_resume_bullets_for_profile(db, profile.id)

    jd_terms = _unique_normalized(
        parsed_jd.required_skills
        + parsed_jd.preferred_skills
        + parsed_jd.required_tools
        + parsed_jd.keywords_for_ats
    )

    scored_results: list[RetrievedEvidence] = []

    for bullet in bullets:
        score, matched_terms = _score_bullet(
            bullet_text=bullet.bullet_text,
            bullet_skills=bullet.skills,
            bullet_tools=bullet.tools,
            bullet_tags=bullet.tags,
            jd_terms=jd_terms,
        )

        if score > 0:
            scored_results.append(
                RetrievedEvidence(
                    bullet_id=bullet.id,
                    section=bullet.section,
                    title=bullet.title,
                    organization=bullet.organization,
                    bullet_text=bullet.bullet_text,
                    matched_terms=matched_terms,
                    score=score,
                )
            )

    scored_results.sort(key=lambda x: (-x.score, x.section, x.bullet_id))

    return {
        "profile_id": profile.id,
        "profile_name": profile.full_name,
        "total_bullets_considered": len(bullets),
        "top_evidence": scored_results[:limit],
    }