# 🛠️ Day 4 — Tool Use & Structured Output

A practical AI project demonstrating **LLM tool calling** using the **Groq API**, **JSON Schema**, **Pydantic validation**, and a **Streamlit UI**.

The project uses a simple calculator as an external Python tool. The LLM decides when the calculator is needed, generates structured arguments, Python validates them with Pydantic, executes the calculator, and sends the result back to the LLM.

---

## 🎯 Learning Objectives

By completing this project, I learned:

* Function/tool calling
* JSON Schema tool definitions
* Structured LLM outputs
* Pydantic schema validation
* Connecting LLMs with Python functions
* Tool execution
* Tool results
* The **Reason → Act → Observe** concept
* Separating backend logic from UI
* Building a Streamlit interface for an AI application

---

## 🧠 Project Concept

The application allows a user to ask mathematical questions in natural language.

For example:

> What is 125 multiplied by 48?

Instead of asking the LLM to calculate the answer directly, the LLM can call a Python calculator tool.

### Flow

```text
User Question
      │
      ▼
Streamlit UI
      │
      ▼
Groq LLM
      │
      ▼
Tool Call
      │
      ▼
JSON Arguments
      │
      ▼
Pydantic Validation
      │
      ▼
Python Calculator
      │
      ▼
Tool Result
      │
      ▼
Groq LLM
      │
      ▼
Final Answer
      │
      ▼
Streamlit UI
```

---

## 🏗️ Architecture

The project separates the user interface from the AI/tool logic.

```text
Day4-Tool-Use/
│
├── app.py
├── ui.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### `app.py`

Contains the backend logic:

* Groq client
* Calculator function
* Pydantic schema
* JSON Schema tool definition
* LLM tool calling
* Tool execution
* Tool result handling

### `ui.py`

Contains the Streamlit interface:

* User input
* Calculate button
* AI response
* Tool execution information
* Calculator result
* Learning explanation

---

## 🔧 Technologies Used

* Python
* Groq API
* `openai/gpt-oss-20b`
* Pydantic
* Streamlit
* python-dotenv
* JSON Schema

---

## 🛠️ Calculator Tool

The project implements a Python calculator supporting four operations:

```text
add
subtract
multiply
divide
```

Example:

```python
calculator(
    a=125,
    b=48,
    operation="multiply"
)
```

Result:

```text
6000
```

Division by zero is also handled safely.

---

## 📋 Pydantic Validation

The tool arguments are validated using Pydantic.

```python
class CalculatorInput(BaseModel):
    a: float
    b: float
    operation: str
```

When the LLM generates:

```json
{
    "a": 125,
    "b": 48,
    "operation": "multiply"
}
```

Pydantic validates the structure before the Python calculator executes.

This creates a safety layer between the LLM and the Python function.

---

## 📐 JSON Schema

The calculator is exposed to the LLM through a JSON Schema tool definition.

Example:

```json
{
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform basic mathematical calculations.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number"
                },
                "b": {
                    "type": "number"
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ]
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
```

The schema tells the LLM:

* What the tool is called
* What the tool does
* Which arguments are required
* Which operations are allowed

---

## 🔄 Tool Calling Process

### Step 1 — User asks a question

```text
What is 125 multiplied by 48?
```

### Step 2 — LLM receives the question

The LLM determines that a calculation is required.

### Step 3 — LLM requests the calculator

The LLM generates a tool call similar to:

```json
{
    "a": 125,
    "b": 48,
    "operation": "multiply"
}
```

### Step 4 — Pydantic validates the arguments

The application validates the generated arguments.

### Step 5 — Python executes the tool

```python
calculator(125, 48, "multiply")
```

Result:

```text
6000
```

### Step 6 — Tool result goes back to the LLM

```text
6000
```

### Step 7 — LLM generates the final response

```text
125 multiplied by 48 is 6000.
```

### Step 8 — Streamlit displays the result

The UI displays both the final answer and the tool execution information.

---

## 🖥️ Streamlit UI

The application provides a simple interface where users can enter questions such as:

```text
What is 100 + 50?
```

```text
Calculate 12 multiplied by 8.
```

```text
What is 100 divided by 4?
```

The interface also displays:

* AI answer
* Tool name
* Tool arguments
* Calculator result

---

## 📸 Example

### User Input

```text
What is 125 multiplied by 48?
```

### Tool Call

```text
Tool: calculator

Arguments:
{
    "a": 125,
    "b": 48,
    "operation": "multiply"
}
```

### Tool Result

```text
6000
```

### Final Answer

```text
125 multiplied by 48 is 6000.
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit your API key to GitHub.

The `.env` file should be included in `.gitignore`.

---

## 📦 Installation

Install the required packages:

```powershell
python -m pip install groq python-dotenv pydantic streamlit
```

Or install from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Run the Application

Navigate to the project:

```powershell
cd E:\AI-Roadmap\Day4-Tool-Use
```

Start Streamlit:

```powershell
python -m streamlit run ui.py
```

The Streamlit application will open in the browser.

---

## 🧪 Test Cases

Try the following questions:

### Addition

```text
What is 100 + 50?
```

Expected:

```text
150
```

### Subtraction

```text
What is 100 - 35?
```

Expected:

```text
65
```

### Multiplication

```text
What is 12 multiplied by 8?
```

Expected:

```text
96
```

### Division

```text
What is 100 divided by 4?
```

Expected:

```text
25
```

### Division by Zero

```text
What is 100 divided by 0?
```

Expected behavior:

```text
Cannot divide by zero.
```

---

## 🧩 Key Concepts Learned

### 1. Function Calling

LLMs can request external functions instead of generating every answer themselves.

### 2. JSON Schema

A schema defines the structure of arguments that the tool accepts.

### 3. Pydantic

Pydantic validates the arguments generated by the LLM before they reach the Python function.

### 4. Tool Execution

The actual calculation is performed by deterministic Python code.

### 5. Tool Results

The result of the Python function is sent back to the LLM.

### 6. Reason → Act → Observe

Conceptually:

```text
Reason
  ↓
Act
  ↓
Observe
  ↓
Respond
```

The LLM decides whether a tool is required, the application executes it, and the LLM uses the result to produce the final response.

---

## 💡 Why Use Tools?

LLMs are good at understanding natural language, but external tools are useful for tasks that should be performed deterministically.

Examples:

```text
Calculator
Weather API
Database
Web Search
File Search
Code Execution
APIs
```

A calculator is a simple example of connecting an LLM with an external capability.

---

## 🚀 Future Improvements

Possible extensions for this project:

* Add a weather tool
* Add multiple tools
* Add currency conversion
* Add web search
* Add calculator history
* Add chat history
* Add tool execution logs
* Add FastAPI backend
* Connect Streamlit to FastAPI
* Add authentication
* Add LangChain tools
* Add LangGraph agent workflow

---

## 📚 Day 4 Checklist

* [x] Function calling
* [x] JSON Schema
* [x] Pydantic validation
* [x] Python calculator tool
* [x] LLM tool selection
* [x] Tool execution
* [x] Tool result returned to LLM
* [x] Final LLM response
* [x] Streamlit UI
* [x] Separate UI and backend logic
* [x] Error handling
* [x] Division-by-zero protection

---

## 👨‍💻 Author

**Muhammad Khizer Hayat**

BS Information Technology
AI/ML Developer | Python | RAG | LangChain | LangGraph

GitHub:
https://github.com/Muhammad-Khizer-Hayat

Portfolio:
https://khizer-portfolio-sepia.vercel.app/

---

## ⭐ Project Summary

This project demonstrates how an LLM can interact with a real Python function through **tool calling**.

The main architecture is:

```text
LLM
 ↓
Tool Selection
 ↓
Structured JSON
 ↓
Pydantic Validation
 ↓
Python Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Response
```

This is a fundamental building block for modern **AI agents and agentic applications**.

````

You can save this directly as:

```text
E:\AI-Roadmap\Day4-Tool-Use\README.md
````

For the next step, your **Day 4 project is ready for GitHub** after we verify `git status` and make sure `.env` is not being tracked.
