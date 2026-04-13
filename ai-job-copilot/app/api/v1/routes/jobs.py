from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.api_models import JDParseRequest, ParsedJDResponse
from app.services.jd_service import parse_and_store_jd

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