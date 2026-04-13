from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ParsedJD:
    role_title: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    seniority: Optional[str] = None
    employment_type: Optional[str] = None
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    qualifications: List[str] = field(default_factory=list)
    keywords_for_ats: List[str] = field(default_factory=list)
    raw_text: str = ""
    source_url: Optional[str] = None
    parser_used: str = "unknown"