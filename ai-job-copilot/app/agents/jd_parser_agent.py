def parse_job_description(jd_text: str) -> dict:
    text = jd_text.lower()

    skills = []
    tools = []

    possible_skills = [
        "python",
        "sql",
        "machine learning",
        "communication",
        "etl",
        "data analysis",
        "nlp",
        "aws",
        "azure",
        "spark"
    ]

    possible_tools = [
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "power bi",
        "tableau",
        "databricks",
        "azure data factory",
        "aws"
    ]

    for skill in possible_skills:
        if skill in text:
            skills.append(skill)

    for tool in possible_tools:
        if tool in text:
            tools.append(tool)

    return {
        "role_title": "Data Scientist" if "data scientist" in text else "",
        "company_name": "",
        "seniority": "",
        "skills": skills,
        "tools": tools,
        "responsibilities": [],
        "qualifications": []
    }