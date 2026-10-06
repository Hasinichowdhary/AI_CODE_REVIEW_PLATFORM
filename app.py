import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Code Review Platform",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0b1220;
    color: #f8fafc;
}

.main {
    background-color: #0b1220;
}

h1, h2, h3 {
    color: #ffffff !important;
}

p, li {
    color: #e2e8f0 !important;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.section-title {
    font-size: 26px;
    font-weight: 650;
    color: #ffffff;
    margin-top: 25px;
    margin-bottom: 15px;
}

.info-box {
    background-color: #111c33;
    border: 1px solid #263858;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.result-box {
    background-color: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 25px;
    margin-top: 20px;
}

.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

textarea {
    background-color: #111827 !important;
    color: #ffffff !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
}

.stTextArea textarea {
    background-color: #111827 !important;
    color: #ffffff !important;
}

.stSelectbox div {
    color: #ffffff;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li {
    color: #cbd5e1 !important;
}

.stMarkdown code {
    background: transparent !important;
    color: #e2e8f0 !important;
    padding: 0 !important;
    border: none !important;
    font-family: inherit !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# GEMINI MODELS
# --------------------------------------------------

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]

# --------------------------------------------------
# CLEAN AI RESPONSE
# --------------------------------------------------

def clean_review(text):
    if not text:
        return ""

    text = text.replace("```python", "")
    text = text.replace("```Python", "")
    text = text.replace("```", "")
    text = text.replace("`", "")

    return text.strip()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🤖 AI Code Review Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your code with Gemini AI and get clear improvement suggestions.</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🤖 AI Code Review")

    st.markdown("---")

    st.markdown("### What it checks")

    st.markdown("""
    - 🐞 Bugs and errors
    - 🔐 Security issues
    - ⚡ Performance
    - 🧹 Code quality
    - 💡 Improvement suggestions
    """)

    st.markdown("---")

    st.markdown("### Session Statistics")

    st.metric(
        "Reviews Created",
        len(st.session_state.history)
    )

    st.markdown("---")

    st.markdown("Powered by Gemini AI")

# --------------------------------------------------
# API KEY CHECK
# --------------------------------------------------

if not API_KEY:

    st.error(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )

    st.stop()

# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# CODE REVIEW SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">💻 Code Review</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="info-box">Paste your code below and select the programming language.</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# LANGUAGE
# --------------------------------------------------

language = st.selectbox(
    "Programming Language",
    [
        "Python",
        "JavaScript",
        "Java",
        "C",
        "C++",
        "C#",
        "HTML",
        "CSS",
        "SQL",
        "Other"
    ]
)

# --------------------------------------------------
# CODE INPUT
# --------------------------------------------------

code = st.text_area(
    "Paste your code here",
    height=350,
    placeholder="Enter your code..."
)

# --------------------------------------------------
# REVIEW BUTTON
# --------------------------------------------------

review_button = st.button(
    "🔍 Review Code"
)

# --------------------------------------------------
# REVIEW PROCESS
# --------------------------------------------------

if review_button:

    if not code.strip():

        st.warning(
            "Please enter some code before starting the review."
        )

    else:

        prompt = f"""
You are an expert software code reviewer.

Review the following {language} code carefully.

CODE:

{code}

Provide a professional and easy-to-understand code review.

Use exactly these sections:

1. Overall Assessment

2. Bugs and Errors

3. Security Issues

4. Performance

5. Code Quality

6. Suggestions

7. Improved Code

Also provide a Code Quality Score from 1 to 10.

Important formatting rules:

- Do NOT use backticks.
- Do NOT use Markdown inline code.
- Do NOT use Markdown code blocks.
- Do NOT use syntax highlighting.
- Do NOT put code names inside special formatting.
- Keep technical names as normal plain text.
- Make the response clean and professional.
- Clearly explain any bugs.
- If there are no security problems, say:
  No major security issues found.
- If there are no bugs, say:
  No major bugs found.
"""

        successful_review = False
        last_error = None

        # --------------------------------------------------
        # TRY AVAILABLE MODELS
        # --------------------------------------------------

        with st.spinner("🤖 AI is reviewing your code..."):

            for model_name in MODELS:

                try:

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )

                    review = clean_review(response.text)

                    if review:

                        successful_review = True

                        # ------------------------------------------
                        # DISPLAY RESULT
                        # ------------------------------------------

                        st.markdown(
                            '<div class="section-title">📋 Review Results</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            '<div class="result-box">',
                            unsafe_allow_html=True
                        )

                        st.markdown(review)

                        st.markdown(
                            '</div>',
                            unsafe_allow_html=True
                        )

                        # ------------------------------------------
                        # SAVE HISTORY
                        # ------------------------------------------

                        st.session_state.history.append(
                            {
                                "language": language,
                                "code": code,
                                "review": review,
                                "model": model_name
                            }
                        )

                        break

                except Exception as e:

                    last_error = str(e)

                    continue

        # --------------------------------------------------
        # IF ALL MODELS FAIL
        # --------------------------------------------------

        if not successful_review:

            st.error(
                "❌ Could not generate the review."
            )

            if last_error:
                st.warning(
                    "Gemini is temporarily unavailable. "
                    "Please try again in a few seconds."
                )

# --------------------------------------------------
# REVIEW HISTORY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📚 Review History</div>',
    unsafe_allow_html=True
)

st.write(
    "Reviews created during this session."
)

if not st.session_state.history:

    st.info(
        "No reviews yet. Your reviews will appear here."
    )

else:

    for index, item in enumerate(
        reversed(st.session_state.history),
        start=1
    ):

        with st.expander(
            f"Review {index} — {item['language']}"
        ):

            st.markdown("### Reviewed Code")

            st.code(
                item["code"],
                language=item["language"].lower()
            )

            st.markdown("### AI Review")

            st.markdown(
                clean_review(item["review"])
            )

            st.caption(
                f"Model used: {item['model']}"
            )

# --------------------------------------------------
# ABOUT
# --------------------------------------------------

st.markdown(
    '<div class="section-title">ℹ️ About</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">

    <b>AI Code Review Platform</b> helps developers understand
    and improve their code using Gemini AI.

    It checks code quality, bugs, security, performance,
    and provides improvement suggestions.

    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "AI Code Review Platform • Powered by Gemini AI"
)