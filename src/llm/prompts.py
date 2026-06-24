PROFILE_GENERATION_PROMPT = """
You are an expert technical interviewer.

Given:

1. Candidate Resume
2. Job Description

Analyze both and produce:

1. Matched Skills
2. Missing Skills
3. Strengths
4. Weaknesses
5. Suggested Interview Topics
6. Project Discussion Points
7. Overall Summary

Be objective and realistic.

Resume:

{resume_text}

Job Description:

{jd_text}
"""