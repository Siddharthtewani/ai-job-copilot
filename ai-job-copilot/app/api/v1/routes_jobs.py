from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.jd_parser_agent import parse_job_description
from app.services.matching_service import calculate_match
from app.agents.resume_tailor_agent import tailor_resume
from app.agents.resume_parser_agent import extract_resume_profile

router = APIRouter()


class JDRequest(BaseModel):
    jd_text: str
    resume_text: str


@router.post("/parse-jd")
def parse_jd(request: JDRequest):
    parsed = parse_job_description(request.jd_text)
    return {"parsed": parsed}


@router.post("/analyze")
def analyze_jd(request: JDRequest):
    parsed = parse_job_description(request.jd_text)
    profile = extract_resume_profile(request.resume_text)

    match = calculate_match(parsed, profile)
    tailored = tailor_resume(parsed, profile)

    return {
        "parsed_jd": parsed,
        "match_analysis": match,
        "resume_improvement": tailored
    }