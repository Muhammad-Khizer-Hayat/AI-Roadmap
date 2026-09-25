# Day 3 — Prompt Engineering Basics

## 📌 Overview

This project is part of my AI learning roadmap.

The goal of Day 3 was to understand the fundamentals of **Prompt Engineering** and observe how different prompting techniques affect the output of a Large Language Model (LLM).

I used the **Groq API** with the `openai/gpt-oss-20b` model and Python.

---

## 🎯 Learning Objectives

During this project, I practiced:

* Zero-shot prompting
* Few-shot prompting
* System prompts
* User prompts
* Structured JSON output
* Prompt constraints
* Iterative prompt refinement
* Reusable prompt templates
* Comparing LLM outputs

---

## 🛠️ Technologies Used

* Python 3.11
* Groq API
* Groq Python SDK
* `python-dotenv`
* JSON
* LLM Prompt Engineering

---

## 📁 Project Structure

```text
Day3-Prompt-Engineering/
│
├── .venv/
├── .env
├── .gitignore
├── app.py
└── README.md
```

### Files

| File         | Purpose                                       |
| ------------ | --------------------------------------------- |
| `app.py`     | Main Python application                       |
| `.env`       | Stores the Groq API key                       |
| `.gitignore` | Prevents sensitive files from being committed |
| `README.md`  | Project documentation                         |
| `.venv/`     | Python virtual environment                    |

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

The API key should **never be hard-coded in Python or committed to GitHub**.

The `.gitignore` file contains:

```text
.venv/
.env
__pycache__/
```

---

# 🧠 Prompt Engineering Experiment

The same job description was analyzed using three different prompting techniques.

### Job Description

```text
We are looking for a Python AI Developer with experience
in LangChain, LangGraph, FastAPI and RAG systems.
The candidate should have experience building AI applications
and REST APIs.
```

---

# 1. Zero-Shot Prompting

The model was given the task without examples.

```text
Analyze the following job description and identify the
important technical skills.
```

### Result

The model produced a detailed response containing:

* Python
* LangChain
* LangGraph
* RAG
* FastAPI
* REST APIs
* Docker
* CI/CD
* Git
* Cloud platforms
* Vector databases
* Embeddings

### Observation

The model added several technologies that were **not explicitly mentioned** in the job description.

This demonstrated that a broad prompt gives the model more freedom to interpret the task.

---

# 2. Few-Shot Prompting

An example was provided before the actual task.

Example:

```text
Job Description:
We need a Python developer with experience in Django,
PostgreSQL and REST APIs.

Skills:
- Python
- Django
- PostgreSQL
- REST APIs
```

The model was then asked to analyze the actual job description.

### Result

The model returned:

```text
- Python
- LangChain
- LangGraph
- FastAPI
- RAG
- REST APIs
```

### Observation

The model followed the example more closely and produced a concise list of relevant skills.

This demonstrated how examples can guide the model toward a desired response pattern.

---

# 3. Structured Prompting

The third prompt explicitly requested JSON.

The model was instructed to return:

```json
{
    "skills": [],
    "frameworks": [],
    "technologies": [],
    "ai_concepts": []
}
```

### Result

```json
{
    "skills": [
        "AI applications",
        "REST APIs"
    ],
    "frameworks": [
        "LangChain",
        "LangGraph",
        "FastAPI"
    ],
    "technologies": [
        "Python"
    ],
    "ai_concepts": [
        "RAG"
    ]
}
```

### Observation

The structured output was easier for a Python application to process.

For example:

```python
data["frameworks"]
```

can directly access the frameworks.

---

# 📊 Comparison

| Technique  | Examples | Output Format    | Control |
| ---------- | -------: | ---------------- | ------- |
| Zero-shot  |       No | Free-form        | Low     |
| Few-shot   |      Yes | Based on example | Medium  |
| Structured | Optional | JSON             | High    |

---

# 🔄 Iterative Prompt Refinement

After testing the first structured prompt, I identified a problem:

The model could potentially infer or add information that was not explicitly present in the job description.

I improved the prompt by adding constraints such as:

```text
1. Do NOT add information that is not explicitly mentioned.
2. Do NOT infer additional technologies.
3. Do NOT recommend additional skills.
4. Preserve the original technology names.
5. Return ONLY valid JSON.
6. Do not use Markdown.
7. Do not add explanations.
```

This demonstrates an important prompt engineering workflow:

```text
Write Prompt
     ↓
Run LLM
     ↓
Observe Output
     ↓
Identify Problem
     ↓
Add Constraints
     ↓
Run Again
     ↓
Compare Results
```

---

# 🧩 System vs User Prompt

The project also uses different message roles.

### System Prompt

```python
{
    "role": "system",
    "content": "You are an expert technical recruiter."
}
```

The system prompt defines the model's behavior and role.

### User Prompt

```python
{
    "role": "user",
    "content": prompt
}
```

The user prompt contains the actual task and input.

Conceptually:

```text
System
  ↓
Defines behavior

User
  ↓
Provides task

LLM
  ↓
Generates response
```

---

# 🐍 Python and JSON

The LLM initially returns JSON as text.

For example:

```python
content = response.choices[0].message.content
```

The JSON string can then be converted into a Python dictionary:

```python
import json

data = json.loads(content)
```

Now Python can access individual fields:

```python
data["skills"]
data["frameworks"]
data["technologies"]
data["ai_concepts"]
```

This is an important pattern for building AI applications.

---

# 💡 Key Lessons

### 1. Clear instructions matter

A vague prompt can produce broad or unexpected results.

### 2. Examples can guide behavior

Few-shot prompting gives the model an example of the expected pattern.

### 3. Structured output improves reliability

JSON makes LLM output easier for software to process.

### 4. Constraints reduce unwanted output

Instructions such as:

```text
Do not infer.
Do not add information.
Return only JSON.
```

can make the output more controlled.

### 5. Prompt engineering is iterative

A good prompt is often developed through repeated testing and refinement.

---

# 🚀 Future Improvements

Possible improvements for this project include:

* Add more few-shot examples
* Compare different system prompts
* Experiment with temperature values
* Add JSON validation
* Handle invalid JSON automatically
* Allow users to enter their own job descriptions
* Build a Streamlit interface
* Compare multiple LLM models
* Measure output consistency across multiple runs

---

# ▶️ How to Run

Clone/download the project and create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install groq python-dotenv
```

Add the API key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
```

Run:

```powershell
python app.py
```

---

# 📚 Day 3 Summary

This project demonstrated how different prompt designs can produce significantly different LLM behavior.

The main progression was:

```text
Zero-shot
   ↓
Few-shot
   ↓
Structured output
   ↓
Constraint-based prompting
   ↓
Iterative refinement
```

This foundation will be useful for later AI projects involving:

* RAG
* AI agents
* LangChain
* LangGraph
* CV/job matching
* Chatbots
* Structured LLM workflows

---

