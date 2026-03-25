def calculate_match(parsed_jd: dict, profile: dict):
    jd_skills = set([s.lower() for s in parsed_jd.get("skills", [])])
    jd_tools = set([t.lower() for t in parsed_jd.get("tools", [])])

    user_skills = set([s.lower() for s in profile.get("skills", [])])
    user_tools = set([t.lower() for t in profile.get("tools", [])])

    matched_skills = jd_skills.intersection(user_skills)
    matched_tools = jd_tools.intersection(user_tools)

    total_required = len(jd_skills) + len(jd_tools)
    total_matched = len(matched_skills) + len(matched_tools)

    score = (total_matched / total_required) * 100 if total_required > 0 else 0

    missing_skills = jd_skills - user_skills
    missing_tools = jd_tools - user_tools

    return {
        "match_score": round(score, 2),
        "matched_skills": list(matched_skills),
        "matched_tools": list(matched_tools),
        "missing_skills": list(missing_skills),
        "missing_tools": list(missing_tools)
    }