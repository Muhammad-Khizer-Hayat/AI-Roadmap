import streamlit as st
from app import ask_llm


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Tool Use ",
    page_icon="🛠️",
    layout="centered"
)


# -----------------------------
# Header
# -----------------------------

st.title("🛠️ AI Tool-Use ")

st.write(
    "Ask a mathematical question and let the LLM "
    "decide when to use the calculator tool."
)

st.divider()


# -----------------------------
# User Input
# -----------------------------

question = st.text_input(
    "Enter your question",
    placeholder="Example: What is 125 multiplied by 48?"
)


# -----------------------------
# Calculate Button
# -----------------------------

if st.button("Calculate", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is processing..."):

            try:

                result = ask_llm(question)

                # Final answer
                st.subheader("🤖 AI Answer")

                st.success(result["answer"])

                # Tool information
                if result["tool_used"]:

                    st.divider()

                    st.subheader("🔧 Tool Execution")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("**Tool Used**")

                        st.code(
                            result["tool_name"]
                        )

                    with col2:

                        st.write("**Calculator Result**")

                        st.metric(
                            "Result",
                            result["result"]
                        )

                    st.write("**Arguments sent to tool**")

                    st.json(result["arguments"])

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# -----------------------------
# Learning Section
# -----------------------------

# with st.expander("📚 How does this work?"):

#     st.markdown(
#         """
# ### Tool Calling Flow

# ```text
# User
#  ↓
# Streamlit UI
#  ↓
# Groq LLM
#  ↓
# Tool Call
#  ↓
# JSON Arguments
#  ↓
# Pydantic Validation
#  ↓
# Python Calculator
#  ↓
# Tool Result
#  ↓
# Groq LLM
#  ↓
# Final Answer
#  ↓
# Streamlit UI
# ````

# ### Concepts

# * Function Calling
# * JSON Schema
# * Pydantic
# * Tool Validation
# * Python Functions as Tools
# * LLM Tool Selection
# * Tool Execution
# * Tool Results
# * Streamlit
#   """
#   )


