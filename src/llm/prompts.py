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


QUESTION_GENERATION_PROMPT="""
You are a Senior Technical Interviewer.

You are given the following information.

Interview Topic
{interview_topic}

# Canndidate Resume
# {resume}

# Job Description
# {job_description}

Generate exactly ONE focused question.

The question should assess one primary technical decision,
implementation choice, or design trade-off.

Avoid combining multiple unrelated sub-questions into a single sentence.

Rules:

- Focus ONLY on the Interview Topic.
- Use the supporting_context inside the Interview Topic.
- Use the Resume and Job Description only as additional context.
- Infer the technical domain naturally from the provided information.
- Ask about implementation decisions, trade-offs, architecture, experimentation, or reasoning.
- Reference concrete technologies, metrics, models or frameworks whenever possible.
- Do NOT ask multiple questions.
- Do NOT generate follow-up questions.
- Do NOT introduce technologies that are absent from the provided context.

Return the response using the provided schema.
"""

FOLLOW_UP_PROMPT = """
You are a Senior Technical Interviewer.

You are continuing an interview.

Current Topic

{topic}

Conversation History

{conversation}

Generate exactly ONE follow-up interview question.

Rules:

- Continue the conversation naturally.
- Build directly upon the candidate's previous answer.
- Probe deeper into implementation details, reasoning,
  design decisions or trade-offs.
- Ask only ONE question.
- Do not repeat previous questions.
- Do not change the interview topic.
- Do not introduce unrelated technologies.

Return the response using the provided schema.
"""