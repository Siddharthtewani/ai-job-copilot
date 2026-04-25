from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.api_models import (
    JDParseRequest,
    MatchRequest,
    MatchResponse,
    MatchResultResponse,
    ParsedJDResponse,
    EvidenceResponse,
)
from app.models.domain_models import ParsedJD
from app.services.jd_service import parse_and_store_jd
from app.services.match_service import calculate_match_score

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "/parse",
    response_model=ParsedJDResponse,
    status_code=status.HTTP_201_CREATED,
)
def parse_job_description(
    payload: JDParseRequest,
    db: Session = Depends(get_db),
) -> ParsedJDResponse:
    try:
        return parse_and_store_jd(
            db=db,
            jd_text=payload.jd_text,
            source_url=payload.source_url,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse job description: {str(exc)}",
        ) from exc


@router.post(
    "/match",
    response_model=MatchResponse,
    status_code=status.HTTP_200_OK,
)
def match_job_description(
    payload: MatchRequest,
    db: Session = Depends(get_db),
) -> MatchResponse:
    try:
        parsed_jd_response = parse_and_store_jd(
            db=db,
            jd_text=payload.jd_text,
            source_url=payload.source_url,
        )

        parsed_jd = ParsedJD(
            role_title=parsed_jd_response.role_title,
            company_name=parsed_jd_response.company_name,
            location=parsed_jd_response.location,
            seniority=parsed_jd_response.seniority,
            employment_type=parsed_jd_response.employment_type,
            required_skills=parsed_jd_response.required_skills,
            preferred_skills=parsed_jd_response.preferred_skills,
            required_tools=parsed_jd_response.required_tools,
            responsibilities=parsed_jd_response.responsibilities,
            qualifications=parsed_jd_response.qualifications,
            keywords_for_ats=parsed_jd_response.keywords_for_ats,
            raw_text=parsed_jd_response.raw_text,
            source_url=parsed_jd_response.source_url,
            parser_used=parsed_jd_response.parser_used,
        )

        match_data = calculate_match_score(
            db=db,
            parsed_jd=parsed_jd,
            evidence_limit=payload.evidence_limit,
        )

        return MatchResponse(
            profile_id=match_data["profile_id"],
            profile_name=match_data["profile_name"],
            parsed_jd=parsed_jd_response,
            match_result=MatchResultResponse(
                overall_score=match_data["match_result"].overall_score,
                matched_skills=match_data["match_result"].matched_skills,
                matched_tools=match_data["match_result"].matched_tools,
                missing_skills=match_data["match_result"].missing_skills,
                missing_tools=match_data["match_result"].missing_tools,
                evidence_count=match_data["match_result"].evidence_count,
            ),
            top_evidence=[
                EvidenceResponse(
                    bullet_id=item.bullet_id,
                    section=item.section,
                    title=item.title,
                    organization=item.organization,
                    bullet_text=item.bullet_text,
                    matched_terms=item.matched_terms,
                    score=item.score,
                )
                for item in match_data["top_evidence"]
            ],
            score_breakdown=match_data["score_breakdown"],
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to match job description: {str(exc)}",
        ) from exc