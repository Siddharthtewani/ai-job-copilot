from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db_models import JobDescriptionDB
from app.models.domain_models import ParsedJD


def create_job_description(db: Session, parsed_jd: ParsedJD) -> JobDescriptionDB:
    job = JobDescriptionDB(
        role_title=parsed_jd.role_title,
        company_name=parsed_jd.company_name,
        location=parsed_jd.location,
        seniority=parsed_jd.seniority,
        employment_type=parsed_jd.employment_type,
        raw_text=parsed_jd.raw_text,
        source_url=parsed_jd.source_url,
        parser_used=parsed_jd.parser_used,
        parsed_json={
            "role_title": parsed_jd.role_title,
            "company_name": parsed_jd.company_name,
            "location": parsed_jd.location,
            "seniority": parsed_jd.seniority,
            "employment_type": parsed_jd.employment_type,
            "required_skills": parsed_jd.required_skills,
            "preferred_skills": parsed_jd.preferred_skills,
            "required_tools": parsed_jd.required_tools,
            "responsibilities": parsed_jd.responsibilities,
            "qualifications": parsed_jd.qualifications,
            "keywords_for_ats": parsed_jd.keywords_for_ats,
        },
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_description_by_id(db: Session, job_id: int) -> JobDescriptionDB | None:
    stmt = select(JobDescriptionDB).where(JobDescriptionDB.id == job_id)
    return db.execute(stmt).scalar_one_or_none()