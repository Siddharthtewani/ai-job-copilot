from sqlalchemy.orm import Session

from app.agents.jd_parser_agent import (
    build_jd_parser_prompt,
    parse_jd_rule_based,
    parse_jd_with_llm,
)
from app.db.repositories.job_repository import create_job_description
from app.models.api_models import ParsedJDResponse
from app.models.domain_models import ParsedJD


def _call_llm_for_jd_parse(prompt: str) -> str:
    """
    Temporary stub.
    Replace this with your real llm_service integration.
    Example:
        from app.services.llm_service import call_openai
        return call_openai(prompt)
    """
    raise NotImplementedError("LLM service not wired yet.")


def parse_and_store_jd(
    db: Session,
    jd_text: str,
    source_url: str | None = None,
) -> ParsedJDResponse:
    if not jd_text or len(jd_text.strip()) < 50:
        raise ValueError("Job description is too short to parse.")

    jd_text = jd_text.strip()

    parsed: ParsedJD
    try:
        prompt = build_jd_parser_prompt(jd_text)
        llm_response_text = _call_llm_for_jd_parse(prompt)
        parsed = parse_jd_with_llm(jd_text, llm_response_text)
    except Exception:
        parsed = parse_jd_rule_based(jd_text)

    parsed.source_url = source_url

    saved = create_job_description(db, parsed)

    return ParsedJDResponse(
        id=saved.id,
        role_title=parsed.role_title,
        company_name=parsed.company_name,
        location=parsed.location,
        seniority=parsed.seniority,
        employment_type=parsed.employment_type,
        required_skills=parsed.required_skills,
        preferred_skills=parsed.preferred_skills,
        required_tools=parsed.required_tools,
        responsibilities=parsed.responsibilities,
        qualifications=parsed.qualifications,
        keywords_for_ats=parsed.keywords_for_ats,
        raw_text=parsed.raw_text,
        source_url=parsed.source_url,
        parser_used=parsed.parser_used,
    )