from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./ai_job_copilot.db"
# Later you can switch this to PostgreSQL, for example:
# DATABASE_URL = "postgresql+psycopg://username:password@localhost:5432/ai_job_copilot"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)