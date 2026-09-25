import json
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


# -----------------------------
# Pydantic Input Schema
# -----------------------------

class CalculatorInput(BaseModel):
    a: float = Field(description="First number")
    b: float = Field(description="Second number")
    operation: str = Field(
        description="Operation: add, subtract, multiply, or divide"
    )


# -----------------------------
# Calculator Tool
# -----------------------------

def calculator(a: float, b: float, operation: str) -> float:

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a / b

    else:
        raise ValueError(f"Unknown operation: {operation}")


# -----------------------------
# Tool Definition
# -----------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform basic mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "Mathematical operation"
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    }
]


# -----------------------------
# LLM + Tool Calling
# -----------------------------

def ask_llm(user_question: str):

    messages = [
        {
            "role": "system",
            "content": """
You are a helpful mathematical assistant.

Use the calculator tool whenever a calculation is required.

After receiving the tool result, explain the answer clearly.
"""
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    # First LLM request
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # No tool required
    if not assistant_message.tool_calls:

        return {
            "answer": assistant_message.content,
            "tool_used": False,
            "tool_name": None,
            "arguments": None,
            "result": None
        }

    # Add assistant tool request
    messages.append(assistant_message)

    tool_name = None
    arguments = None
    tool_result = None

    # Execute requested tools
    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        # Validate arguments
        validated_input = CalculatorInput(**arguments)

        # Execute calculator
        tool_result = calculator(
            validated_input.a,
            validated_input.b,
            validated_input.operation
        )

        # Send result back to LLM
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
            }
        )

    # Second LLM request
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools
    )

    final_answer = final_response.choices[0].message.content

    return {
        "answer": final_answer,
        "tool_used": True,
        "tool_name": tool_name,
        "arguments": arguments,
        "result": tool_result
    }
