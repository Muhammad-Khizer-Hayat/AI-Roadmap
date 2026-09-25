import os
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")


# Create Groq client
client = Groq(api_key=api_key)


# Same task for all experiments
job_description = """
We are looking for a Python AI Developer with experience
in LangChain, LangGraph, FastAPI and RAG systems.
The candidate should have experience building AI applications
and REST APIs.
"""
# 1. ZERO-SHOT PROMPT

zero_shot_prompt = f"""
Analyze the following job description and identify the
important technical skills.

Job Description:

{job_description}
"""
# 2. FEW-SHOT PROMPT

few_shot_prompt = f"""
Identify the important technical skills from a job description.

Example:

Job Description:
We need a Python developer with experience in Django,
PostgreSQL and REST APIs.

Skills:
- Python
- Django
- PostgreSQL
- REST APIs

Now analyze this job description:

{job_description}

Return the important technical skills.
"""

# 3. STRUCTURED PROMPT

structured_prompt = f"""
Analyze the following job description.

Extract the technical skills.

Return ONLY valid JSON using exactly this structure:

{{
    "skills": [],
    "frameworks": [],
    "technologies": [],
    "ai_concepts": []
}}

Rules:

1. Do not add explanations.
2. Do not use Markdown.
3. Put Python under technologies.
4. Put LangChain and LangGraph under frameworks.
5. Put RAG under ai_concepts.
6. Put FastAPI under frameworks.

Job Description:

{job_description}
"""


def ask_llm(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert technical recruiter."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# Run all three prompts
zero_shot_result = ask_llm(zero_shot_prompt)
few_shot_result = ask_llm(few_shot_prompt)
structured_result = ask_llm(structured_prompt)


# Display results
print("ZERO-SHOT RESULT")
print(zero_shot_result)


print("FEW-SHOT RESULT")
print(few_shot_result)


print("STRUCTURED RESULT")
print(structured_result)