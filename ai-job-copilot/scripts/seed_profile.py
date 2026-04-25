from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.db.repositories.profile_repository import (
    create_resume_bullet,
    create_user_profile,
    deactivate_existing_profiles,
)

# Ensure tables exist
Base.metadata.create_all(bind=engine)


def main() -> None:
    db = SessionLocal()

    try:
        deactivate_existing_profiles(db)

        profile = create_user_profile(
            db=db,
            full_name="Siddharth Tewani",
            email=None,
            linkedin_url="https://www.linkedin.com/in/siddharth-tewani/",
            github_url="https://github.com/Siddharthtewani",
            professional_summary=(
                "Data Scientist and AI Engineer candidate with experience in machine learning, "
                "data analytics, ETL workflows, NLP, and backend application development. "
                "Built production-style projects using Python, SQL, FastAPI, cloud tooling, "
                "and modern AI workflows."
            ),
            target_roles=[
                "Data Scientist",
                "AI Engineer",
                "Machine Learning Engineer",
                "LLM Engineer",
            ],
            skills=[
                "Python",
                "SQL",
                "Machine Learning",
                "Data Analysis",
                "NLP",
                "ETL",
                "Statistics",
                "LLMs",
                "MLOps",
            ],
            tools=[
                "FastAPI",
                "AWS",
                "Azure",
                "Spark",
                "Pandas",
                "NumPy",
                "Scikit-learn",
                "TensorFlow",
                "Tableau",
                "Power BI",
                "Databricks",
                "PostgreSQL",
            ],
            projects=[
                "ComUnity AI Event Recommender",
                "Stock Volatility Prediction",
                "NLP Student Feedback Analysis",
                "AI Job Copilot",
            ],
        )

        bullets = [
            {
                "section": "experience",
                "title": "Industry Experience Project",
                "organization": "Monash University / Client Project",
                "bullet_text": (
                    "Built ComUnity, a web platform designed to help young people discover "
                    "community events and nearby places using map-based exploration and AI-driven ideas."
                ),
                "skills": ["Python", "Data Analysis"],
                "tools": ["FastAPI", "AWS"],
                "tags": ["community platform", "backend", "web app"],
                "metrics": [],
            },
            {
                "section": "project",
                "title": "AI Job Copilot",
                "organization": "Personal Project",
                "bullet_text": (
                    "Designed a production-style AI job search assistant using FastAPI, structured parsing, "
                    "retrieval logic, and resume-tailoring workflows for Data Scientist and AI Engineer roles."
                ),
                "skills": ["Python", "LLMs", "Machine Learning"],
                "tools": ["FastAPI", "PostgreSQL"],
                "tags": ["job copilot", "llm workflow", "backend"],
                "metrics": [],
            },
            {
                "section": "project",
                "title": "Stock Volatility Prediction",
                "organization": "Academic Project",
                "bullet_text": (
                    "Developed regression and machine learning models to predict monthly stock volatility "
                    "using financial features, feature engineering, and model evaluation workflows."
                ),
                "skills": ["Python", "Machine Learning", "Data Analysis", "Statistics"],
                "tools": ["Pandas", "NumPy", "Scikit-learn"],
                "tags": ["forecasting", "regression", "finance"],
                "metrics": ["R-squared improvement"],
            },
            {
                "section": "project",
                "title": "NLP Student Feedback Analysis",
                "organization": "Academic / Research Project",
                "bullet_text": (
                    "Built NLP-based analysis pipelines to process and interpret open-text student feedback, "
                    "including text preprocessing, tokenization, and insight generation."
                ),
                "skills": ["Python", "NLP", "Data Analysis"],
                "tools": ["Pandas"],
                "tags": ["text analytics", "feedback analysis", "education"],
                "metrics": [],
            },
            {
                "section": "experience",
                "title": "Data Engineering / Analytics Experience",
                "organization": "Professional / Project Experience",
                "bullet_text": (
                    "Worked with ETL-style pipelines, structured datasets, SQL workflows, and analytics tooling "
                    "to clean, transform, and analyze data for decision-making."
                ),
                "skills": ["Python", "SQL", "ETL", "Data Analysis"],
                "tools": ["Spark", "Azure", "Databricks", "Tableau"],
                "tags": ["etl", "analytics engineering", "data workflows"],
                "metrics": [],
            },
            {
                "section": "project",
                "title": "Backend and API Development",
                "organization": "Project Experience",
                "bullet_text": (
                    "Built backend APIs and integrated data-driven functionality using FastAPI, structured models, "
                    "and persistent storage patterns."
                ),
                "skills": ["Python"],
                "tools": ["FastAPI", "PostgreSQL"],
                "tags": ["api development", "backend engineering"],
                "metrics": [],
            },
            {
                "section": "skill_proof",
                "title": "Cloud and Platform Tooling",
                "organization": None,
                "bullet_text": (
                    "Worked with cloud and platform tools including AWS, Azure, Databricks, and PostgreSQL "
                    "across machine learning and data-focused projects."
                ),
                "skills": ["Machine Learning", "ETL"],
                "tools": ["AWS", "Azure", "Databricks", "PostgreSQL"],
                "tags": ["cloud", "platform", "data infrastructure"],
                "metrics": [],
            },
        ]

        for bullet in bullets:
            create_resume_bullet(
                db=db,
                user_profile_id=profile.id,
                section=bullet["section"],
                title=bullet["title"],
                organization=bullet["organization"],
                bullet_text=bullet["bullet_text"],
                skills=bullet["skills"],
                tools=bullet["tools"],
                tags=bullet["tags"],
                metrics=bullet["metrics"],
            )

        print(f"Seed complete. Active profile ID: {profile.id}")

    finally:
        db.close()


if __name__ == "__main__":
    main()