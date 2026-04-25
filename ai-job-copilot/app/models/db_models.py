from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserProfileDB(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    professional_summary: Mapped[str] = mapped_column(Text, nullable=False)
    target_roles: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    tools: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    projects: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    resume_bullets: Mapped[list["ResumeBulletDB"]] = relationship(
        "ResumeBulletDB",
        back_populates="user_profile",
        cascade="all, delete-orphan",
    )


class ResumeBulletDB(Base):
    __tablename__ = "resume_bullets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_profile_id: Mapped[int] = mapped_column(
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    section: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bullet_text: Mapped[str] = mapped_column(Text, nullable=False)

    skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    tools: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    metrics: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user_profile: Mapped["UserProfileDB"] = relationship(
        "UserProfileDB",
        back_populates="resume_bullets",
    )


class JobDescriptionDB(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    seniority: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    parsed_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    parser_used: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class GeneratedArtifactDB(Base):
    __tablename__ = "generated_artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_profile_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    job_description_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("job_descriptions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    artifact_type: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class PipelineRunDB(Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_profile_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    job_description_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("job_descriptions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    run_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="started")
    inputs_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    outputs_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )