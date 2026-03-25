from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.jd_parser_agent import parse_job_description
from app.services.resume_service import get_user_profile
from app.services.matching_service import calculate_match

router = APIRouter()


class JDRequest(BaseModel):
    jd_text: str


@router.post("/parse-jd")
def parse_jd(request: JDRequest):
    parsed = parse_job_description(request.jd_text)
    return {"parsed": parsed}


@router.post("/analyze")
def analyze_jd(request: JDRequest):
    parsed = parse_job_description(request.jd_text)
    profile = get_user_profile()
    match = calculate_match(parsed, profile)

    return {
        "parsed_jd": parsed,
        "match_analysis": match
    }