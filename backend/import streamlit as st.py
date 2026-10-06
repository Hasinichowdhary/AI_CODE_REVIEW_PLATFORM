import streamlit as st

st.set_page_config(
    page_title="AI Code Review Platform",
    page_icon="🤖"
)

st.title("🤖 AI Code Review Platform")

st.write("Enter your code below and get AI-powered code review.")

code = st.text_area(
    "Enter your code:",
    height=300,
    placeholder="Write or paste your code here..."
)

if st.button("Review Code"):
    if code.strip():
        st.subheader("Code Review")
        st.write("✅ Code received successfully!")
        st.write("AI analysis will be added here.")
    else:
        st.warning("Please enter some code first.")