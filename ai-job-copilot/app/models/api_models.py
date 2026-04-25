from typing import Any, List, Optional

from pydantic import BaseModel, Field


class JDParseRequest(BaseModel):
    jd_text: str = Field(..., min_length=50, description="Raw job description text")
    source_url: Optional[str] = Field(default=None, description="Optional source URL")


class ParsedJDResponse(BaseModel):
    id: Optional[int] = None
    role_title: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    seniority: Optional[str] = None
    employment_type: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)
    keywords_for_ats: List[str] = Field(default_factory=list)
    raw_text: str
    source_url: Optional[str] = None
    parser_used: str


class MatchRequest(BaseModel):
    jd_text: str = Field(..., min_length=50, description="Raw job description text")
    source_url: Optional[str] = Field(default=None, description="Optional source URL")
    evidence_limit: int = Field(default=5, ge=1, le=10)


class EvidenceResponse(BaseModel):
    bullet_id: int
    section: str
    title: Optional[str] = None
    organization: Optional[str] = None
    bullet_text: str
    matched_terms: List[str] = Field(default_factory=list)
    score: int


class MatchResultResponse(BaseModel):
    overall_score: float
    matched_skills: List[str] = Field(default_factory=list)
    matched_tools: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    missing_tools: List[str] = Field(default_factory=list)
    evidence_count: int


class MatchResponse(BaseModel):
    profile_id: int
    profile_name: str
    parsed_jd: ParsedJDResponse
    match_result: MatchResultResponse
    top_evidence: List[EvidenceResponse] = Field(default_factory=list)
    score_breakdown: dict[str, Any]


class ErrorResponse(BaseModel):
    detail: str