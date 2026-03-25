def tailor_resume(parsed_jd: dict, profile: dict) -> dict:
    jd_skills = set(parsed_jd.get("skills", []))
    user_skills = set(profile.get("skills", []))

    missing_skills = jd_skills - user_skills

    improved_skills = list(user_skills.union(jd_skills))

    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Consider adding or learning: {skill}")

    return {
        "improved_skills": improved_skills,
        "suggestions": suggestions,
        "summary": f"Resume improved with {len(improved_skills)} relevant skills."
    }