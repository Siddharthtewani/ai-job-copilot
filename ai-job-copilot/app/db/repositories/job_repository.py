from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db_models import ResumeBulletDB, UserProfileDB


def get_active_user_profile(db: Session) -> UserProfileDB | None:
    stmt = select(UserProfileDB).where(UserProfileDB.is_active.is_(True))
    return db.execute(stmt).scalar_one_or_none()


def create_user_profile(
    db: Session,
    *,
    full_name: str,
    email: str | None,
    linkedin_url: str | None,
    github_url: str | None,
    professional_summary: str,
    target_roles: list[str],
    skills: list[str],
    tools: list[str],
    projects: list[str],
    is_active: bool = True,
) -> UserProfileDB:
    profile = UserProfileDB(
        full_name=full_name,
        email=email,
        linkedin_url=linkedin_url,
        github_url=github_url,
        professional_summary=professional_summary,
        target_roles=target_roles,
        skills=skills,
        tools=tools,
        projects=projects,
        is_active=is_active,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def deactivate_existing_profiles(db: Session) -> None:
    profiles = db.query(UserProfileDB).filter(UserProfileDB.is_active.is_(True)).all()
    for profile in profiles:
        profile.is_active = False
    db.commit()


def create_resume_bullet(
    db: Session,
    *,
    user_profile_id: int,
    section: str,
    title: str | None,
    organization: str | None,
    bullet_text: str,
    skills: list[str] | None = None,
    tools: list[str] | None = None,
    tags: list[str] | None = None,
    metrics: list[str] | None = None,
) -> ResumeBulletDB:
    bullet = ResumeBulletDB(
        user_profile_id=user_profile_id,
        section=section,
        title=title,
        organization=organization,
        bullet_text=bullet_text,
        skills=skills or [],
        tools=tools or [],
        tags=tags or [],
        metrics=metrics or [],
    )
    db.add(bullet)
    db.commit()
    db.refresh(bullet)
    return bullet


def get_resume_bullets_for_profile(
    db: Session,
    user_profile_id: int,
) -> list[ResumeBulletDB]:
    stmt = (
        select(ResumeBulletDB)
        .where(ResumeBulletDB.user_profile_id == user_profile_id)
        .order_by(ResumeBulletDB.id.asc())
    )
    return list(db.execute(stmt).scalars().all())