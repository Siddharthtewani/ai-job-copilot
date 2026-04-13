import json
import re
from typing import Any

from app.models.domain_models import ParsedJD


COMMON_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "nlp",
    "data analysis",
    "statistics",
    "etl",
    "spark",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "llms",
    "rag",
    "mlops",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "power bi",
    "tableau",
    "fastapi",
]

COMMON_TOOLS = [
    "python",
    "sql",
    "spark",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "power bi",
    "tableau",
    "databricks",
    "airflow",
    "fastapi",
    "postgresql",
]


def _extract_json_from_text(text: str) -> dict[str, Any]:
    """
    Extract the first JSON object from a raw LLM response.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response.")
    return json.loads(match.group(0))


def _normalize_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    cleaned = []
    seen = set()

    for value in values:
        item = value.strip()
        if not item:
            continue
        key = item.lower()
        if key not in seen:
            seen.add(key)
            cleaned.append(item)
    return cleaned


def _safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    value = data.get(key, default)
    return default if value is None else value


def build_jd_parser_prompt(jd_text: str) -> str:
    return f"""
You are an expert information extraction system for job descriptions.

Extract the job description into a strict JSON object.

Rules:
- Return valid JSON only
- Do not include markdown
- Do not invent information
- Separate required vs preferred skills when possible
- Keep responsibilities and qualifications concise
- Infer seniority only when strongly implied
- Infer ATS keywords from explicit role requirements

Return this JSON schema exactly:
{{
  "role_title": "string",
  "company_name": "string or null",
  "location": "string or null",
  "seniority": "string or null",
  "employment_type": "string or null",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "required_tools": ["string"],
  "responsibilities": ["string"],
  "qualifications": ["string"],
  "keywords_for_ats": ["string"]
}}

Job description:
\"\"\"
{jd_text}
\"\"\"
""".strip()


def parse_jd_with_llm(jd_text: str, llm_response_text: str) -> ParsedJD:
    data = _extract_json_from_text(llm_response_text)

    return ParsedJD(
        role_title=_safe_get(data, "role_title", "Unknown Role"),
        company_name=_safe_get(data, "company_name"),
        location=_safe_get(data, "location"),
        seniority=_safe_get(data, "seniority"),
        employment_type=_safe_get(data, "employment_type"),
        required_skills=_normalize_list(_safe_get(data, "required_skills", [])),
        preferred_skills=_normalize_list(_safe_get(data, "preferred_skills", [])),
        required_tools=_normalize_list(_safe_get(data, "required_tools", [])),
        responsibilities=_normalize_list(_safe_get(data, "responsibilities", [])),
        qualifications=_normalize_list(_safe_get(data, "qualifications", [])),
        keywords_for_ats=_normalize_list(_safe_get(data, "keywords_for_ats", [])),
        raw_text=jd_text,
        parser_used="llm",
    )


def parse_jd_rule_based(jd_text: str) -> ParsedJD:
    text = jd_text.lower()

    role_title = "Unknown Role"
    if "data scientist" in text:
        role_title = "Data Scientist"
    elif "ai engineer" in text:
        role_title = "AI Engineer"
    elif "machine learning engineer" in text or "ml engineer" in text:
        role_title = "Machine Learning Engineer"
    elif "data analyst" in text:
        role_title = "Data Analyst"

    seniority = None
    if "senior" in text:
        seniority = "Senior"
    elif "junior" in text:
        seniority = "Junior"
    elif "mid" in text or "mid-level" in text:
        seniority = "Mid-level"

    employment_type = None
    if "full-time" in text:
        employment_type = "Full-time"
    elif "part-time" in text:
        employment_type = "Part-time"
    elif "contract" in text:
        employment_type = "Contract"

    required_skills = [skill.title() for skill in COMMON_SKILLS if skill in text]
    required_tools = [tool.title() for tool in COMMON_TOOLS if tool in text]

    keywords_for_ats = list(dict.fromkeys(required_skills + required_tools))

    return ParsedJD(
        role_title=role_title,
        company_name=None,
        location=None,
        seniority=seniority,
        employment_type=employment_type,
        required_skills=required_skills,
        preferred_skills=[],
        required_tools=required_tools,
        responsibilities=[],
        qualifications=[],
        keywords_for_ats=keywords_for_ats,
        raw_text=jd_text,
        parser_used="rule_based",
    )