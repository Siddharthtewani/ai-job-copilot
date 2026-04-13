from fastapi import FastAPI

from app.api.v1.routes.jobs import router as jobs_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="AI Job Copilot")

Base.metadata.create_all(bind=engine)

app.include_router(jobs_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}