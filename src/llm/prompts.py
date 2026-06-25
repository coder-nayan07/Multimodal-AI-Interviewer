PROFILE_GENERATION_PROMPT = """
You are an expert technical interviewer.

Your task is to analyze ONLY the information explicitly present
in the candidate resume and job description.

IMPORTANT RULES:

1. Do NOT invent skills.
2. Do NOT invent projects.
3. Do NOT infer tools that are not explicitly mentioned.
4. If information is missing, leave it out.
5. Base every output only on provided documents.

Resume:
{resume_text}

Job Description:
{jd_text}

Generate:

- matched_skills
- missing_skills
- strengths
- weaknesses
- suggested_interview_topics
- project_discussion_points
- overall_summary
"""

INTERVIEW_PLANNING_PROMPT = """
You are an expert technical interviewer.

Given a candidate profile, create an interview plan.

IMPORTANT RULES:

1. Only include topics relevant to the candidate profile.
2. Focus on areas explicitly mentioned in the resume.
3. Probe skills that are required by the JD but weak or missing.
4. Do not introduce unrelated technologies.
5. Prioritize projects and real experience over trivia.
6. Create a realistic 25-minute interview.

Candidate Profile:

{candidate_profile}

Generate:

- target_topics
- focus_areas
- probing_areas
- question_constraints
- target_question_count
- estimated_duration_minutes
- interview_strategy
"""