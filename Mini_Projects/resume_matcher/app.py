import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pypdf import PdfReader
import re

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        return text

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

def extract_name(resume_text):
    lines = resume_text.strip().splitlines()

    if lines:
        return lines[0].strip()

    return "Unknown Candidate"

def match_requirements(resume_text, requirements):
    matched_requirements = []

    for requirement in requirements:
        pattern = r"\b" + re.escape(requirement.lower()) + r"\b"

        if re.search(pattern, resume_text.lower()):
            matched_requirements.append(requirement)

    return matched_requirements

st.title("Resume Requirement Matcher")
st.write("Upload resumes and check how well they match the job requirements.")

uploaded_files = st.file_uploader(
    "Upload your resumes",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

requirements_input = st.text_area(
    "Enter job requirements (one per line)",
    placeholder="Python\nMachine Learning\nPandas\nSQL\nTensorFlow"
)

requirements = [
    req.strip()
    for req in requirements_input.splitlines()
    if req.strip()
]

if requirements:
    st.write("Requirements:", requirements) 

if uploaded_files and requirements:
    results = []

    for file in uploaded_files:
        text = extract_text(file)

        matched = match_requirements(text, requirements)

        results.append({
            "Candidate": extract_name(text),
            "Matched": len(matched),
            "Total": len(requirements),
            "Score": (len(matched) / len(requirements)) * 100
        })

    df = pd.DataFrame(results)
    df["Score"] = df["Score"].round(2)

    st.subheader("Resume Matching Results")
    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df["Candidate"], df["Matched"])

    ax.set_xlabel("Candidates")
    ax.set_ylabel("Requirements Matched")
    ax.set_title("Resume Requirement Matching")

    ax.set_ylim(0, len(requirements))

    st.pyplot(fig)

    best_candidate = df.loc[df["Matched"].idxmax()]
    if best_candidate["Matched"] >= 7:
        st.success(
            f" Best Match: {best_candidate['Candidate']} "
            f"matches {best_candidate['Matched']} out of "
            f"{best_candidate['Total']} requirements "
            f"({best_candidate['Score']}%)."
        )
    else:
        st.warning(
            f" Highest Match: {best_candidate['Candidate']} "
            f"matches {best_candidate['Matched']} out of "
            f"{best_candidate['Total']} requirements "
            f"({best_candidate['Score']}%). "
            f"No candidate reached the minimum requirement of 7."
        )