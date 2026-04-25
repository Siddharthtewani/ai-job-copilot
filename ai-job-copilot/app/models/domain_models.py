from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedJD:
    role_title: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    seniority: Optional[str] = None
    employment_type: Optional[str] = None
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    qualifications: list[str] = field(default_factory=list)
    keywords_for_ats: list[str] = field(default_factory=list)
    raw_text: str = ""
    source_url: Optional[str] = None
    parser_used: str = "unknown"


@dataclass
class CandidateProfile:
    profile_id: int
    full_name: str
    professional_summary: str
    target_roles: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)


@dataclass
class EvidenceSnippet:
    bullet_id: int
    section: str
    title: Optional[str]
    organization: Optional[str]
    bullet_text: str
    matched_terms: list[str] = field(default_factory=list)
    score: int = 0


@dataclass
class MatchResult:
    overall_score: float
    matched_skills: list[str] = field(default_factory=list)
    matched_tools: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    missing_tools: list[str] = field(default_factory=list)
    evidence_count: int = 0


@dataclass
class TailoredResumeDraft:
    summary: str
    experience_bullets: list[str] = field(default_factory=list)
    project_bullets: list[str] = field(default_factory=list)


@dataclass
class CritiqueResult:
    ats_keyword_coverage: float
    unsupported_claims: list[str] = field(default_factory=list)
    repeated_phrases: list[str] = field(default_factory=list)
    weak_bullets: list[str] = field(default_factory=list)
    generic_wording: list[str] = field(default_factory=list)