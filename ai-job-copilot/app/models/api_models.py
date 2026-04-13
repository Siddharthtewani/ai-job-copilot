from typing import List, Optional

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


class ErrorResponse(BaseModel):
    detail: str