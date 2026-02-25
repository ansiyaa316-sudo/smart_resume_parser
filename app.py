import streamlit as st
import pandas as pd
import json
from parser import parse_resume

st.set_page_config(page_title="Smart Resume Parser", layout="wide")

st.title("🧠 Smart Resume Parser")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1]
    result = parse_resume(uploaded_file, file_type)
    st.subheader("📄 Extracted Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 👤 Basic Info")
        st.write("**Name:**", result.get("name","Not Found"))
        st.write("**Email:**", result.get("email","Not Found"))
        st.write("**Phone:**", result.get("phone","Not Found"))

    with col2:
        st.write("### 🛠 Skills")
        for skill in result.get("skills",[]):
            st.write("-", skill)

    st.write("### 🎓 Education")
    for edu in result.get("education",[]):
        st.write("-", edu)

    st.write("### 💼 Experience")
    for exp in result.get("experience",[]):
        st.write("-", exp)

    # Download buttons
    st.download_button(
        "Download JSON",
        json.dumps(result, indent=4),
        file_name="parsed_resume.json",
        mime="application/json"
    )

    df = pd.DataFrame([result])
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="parsed_resume.csv",
        mime="text/csv"
    )