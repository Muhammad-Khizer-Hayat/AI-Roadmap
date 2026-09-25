import os
import json

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")


# Create Groq client
client = Groq(api_key=api_key)


# Ask the LLM for structured information
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": """
You are a helpful programming teacher.
Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside the JSON.
"""
        },
        {
            "role": "user",
            "content": """
Explain the concept of an API.

Return this exact JSON structure:

{
    "concept": "string",
    "definition": "string",
    "example": "string",
    "important": true
}
"""
        }
    ],
    temperature=0,
)


# Get the generated text
content = response.choices[0].message.content

print("\n===== RAW LLM RESPONSE =====\n")
print(content)


# Convert JSON string into Python dictionary
try:
    data = json.loads(content)

    print("\n===== PARSED PYTHON DATA =====\n")
    print(json.dumps(data, indent=4))

    print("\n===== ACCESSING INDIVIDUAL VALUES =====\n")

    print("Concept:")
    print(data["concept"])

    print("\nDefinition:")
    print(data["definition"])

    print("\nExample:")
    print(data["example"])

    print("\nImportant:")
    print(data["important"])

except json.JSONDecodeError:
    print("\nERROR: The LLM did not return valid JSON.")