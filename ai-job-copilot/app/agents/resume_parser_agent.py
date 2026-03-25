def extract_resume_profile(resume_text: str) -> dict:
    text = resume_text.lower()

    skills = []
    tools = []

    possible_skills = [
        "python", "sql", "machine learning", "etl",
        "data analysis", "nlp", "communication"
    ]

    possible_tools = [
        "pandas", "numpy", "scikit-learn",
        "tensorflow", "aws", "azure", "databricks"
    ]

    for skill in possible_skills:
        if skill in text:
            skills.append(skill)

    for tool in possible_tools:
        if tool in text:
            tools.append(tool)

    return {
        "skills": skills,
        "tools": tools
    }