from fastapi import FastAPI
from app.api.v1.routes_jobs import router as jobs_router

app = FastAPI(title="AI Job Copilot")

app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])


@app.get("/")
def root():
    return {"message": "working"}