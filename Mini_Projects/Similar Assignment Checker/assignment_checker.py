import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import re
from nltk.corpus import stopwords
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords")

st.set_page_config(page_title="Assignment Similarity Checker", layout="wide")

st.title("Assignment Similarity Checker")

st.write("Upload multiple assignments and check their textual similarity "
    "using TF-IDF and Cosine Similarity.")

def extract_text(file):

    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:

            text += page.extract_text() or ""
        return text

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    stop_words = set(stopwords.words("english"))

    words = [word
        for word in words
        if word not in stop_words]
    return " ".join(words)

uploaded_files = st.file_uploader(
    "Upload student assignments",
    type=["txt", "pdf"],
    accept_multiple_files=True)

threshold = st.slider(
    "Similarity threshold (%)",
    min_value=0,
    max_value=100,
    value=70)

if uploaded_files:
    assignments = []
    names = []

    for file in uploaded_files:
        content = extract_text(file)
        content = preprocess_text(content)
        assignments.append(content)
        names.append(file.name)

    st.write("Uploaded assignments:", names)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(assignments)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    results = []

    for i in range(len(names)):

        scores = similarity_matrix[i].copy()

        scores[i] = -1

        most_similar_index = scores.argmax()
        most_similar_score = scores[ most_similar_index ]
        similarity_percentage = round(most_similar_score * 100, 2)

        if similarity_percentage >= threshold:
            status = "High Similarity"
        else:
            status = "Low Similarity"

        results.append({
            "Student": names[i],
            "Most Similar To": names[most_similar_index],
            "Similarity (%)": similarity_percentage,
            "Status": status
        })

    results_df = pd.DataFrame(results)
    st.subheader("Assignment Similarity Results")
    st.dataframe(results_df, use_container_width=True)

    similarity_df = pd.DataFrame(similarity_matrix, index=names, columns=names)

    st.subheader("Similarity Matrix")
    st.dataframe( similarity_df, use_container_width=True)
    st.subheader("Similarity Visualization")
    fig, ax = plt.subplots()

    ax.barh( results_df["Student"], results_df["Similarity (%)"] )
    ax.axvline(threshold, linestyle="--",  label=f"Threshold: {threshold}%")
    ax.set_xlabel("Similarity (%)")
    ax.set_ylabel("Students")
    ax.set_title("Highest Assignment Similarity")
    ax.set_xlim( 0, 100)
    ax.invert_yaxis()
    ax.legend()
    st.pyplot(fig)

    pairs = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            similarity_percentage = round(similarity_matrix[i][j] * 100, 2)

            if similarity_percentage >= threshold:
                pairs.append({
                    "Student 1": names[i],
                    "Student 2": names[j],
                    "Similarity (%)": similarity_percentage
                })

    st.subheader("Potentially Similar Assignment Pairs")

    if pairs:
        pairs_df = pd.DataFrame(pairs)
        st.dataframe(pairs_df, use_container_width=True)

    else:
        st.success(
            "No assignment pairs exceeded "
            "the selected similarity threshold.")

    csv = results_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Results",
        data=csv,
        file_name="assignment_similarity_results.csv",
        mime="text/csv")