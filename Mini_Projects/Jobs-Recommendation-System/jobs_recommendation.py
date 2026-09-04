import streamlit as st
import pandas as pd
import ast
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Job Recommendation System",
    layout="wide"
)


# LOAD DATA
@st.cache_data
def load_data():

    df = pd.read_csv("all_job_post.csv")

    # Convert skill strings into Python lists
    df["job_skill_set"] = df["job_skill_set"].apply(
        ast.literal_eval
    )

    # Create searchable skill text
    df["skills_text"] = df["job_skill_set"].apply(
        lambda skills: " ".join(
            str(skill).lower()
            for skill in skills
        )
    )

    # Combine job title + description + skills
    df["search_text"] = (
        df["job_title"].fillna("") + " " +
        df["job_description"].fillna("") + " " +
        df["skills_text"]
    ).str.lower()

    return df


df = load_data()

# HEADER
st.title("AI Job Recommendation System")

st.markdown(
    """
    ### Find jobs that match your skills, interests and experience.

    This system uses **TF-IDF and Cosine Similarity** to compare
    your profile with job postings and rank the most relevant
    opportunities.
    """
)

st.divider()

# SIDEBAR
st.sidebar.header("👤 Your Profile")

user_skills = st.sidebar.text_area(
    "Your Skills",
    placeholder="Python, SQL, Git, AWS, Machine Learning"
)

user_interests = st.sidebar.text_area(
    "Your Interests",
    placeholder="Artificial Intelligence, Data Science"
)

experience = st.sidebar.slider(
    "Years of Experience",
    min_value=0,
    max_value=20,
    value=0
)

categories = sorted(
    df["category"]
    .dropna()
    .unique()
)

user_category = st.sidebar.selectbox(
    "Preferred Job Category",
    ["Any"] + list(categories)
)

num_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    3,
    15,
    5
)

# HELPER FUNCTIONS
def extract_experience(text):

    patterns = [
        r"(\d+)\+?\s*years?\s+of\s+experience",
        r"(\d+)\+?\s*years?\s+experience",
        r"minimum\s+of\s+(\d+)\s+years?",
        r"at\s+least\s+(\d+)\s+years?"
    ]

    numbers = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text.lower()
        )

        for match in matches: 
            numbers.append(int(match))

    if numbers:
        return min(numbers)

    return 0


def get_matched_skills(user_skills, job_skills):

    user_skill_list = [
        skill.strip().lower()
        for skill in user_skills.split(",")
        if skill.strip()
    ]

    job_skill_list = [
        str(skill).strip().lower()
        for skill in job_skills
    ]

    matched = []

    for user_skill in user_skill_list:

        for job_skill in job_skill_list:

            if user_skill in job_skill or job_skill in user_skill:

                matched.append(user_skill)
                break

    return list(set(matched))


def get_missing_skills(user_skills, job_skills):

    user_skill_list = [
        skill.strip().lower()
        for skill in user_skills.split(",")
        if skill.strip()
    ]

    job_skill_list = [
        str(skill).strip().lower()
        for skill in job_skills
    ]

    missing = []

    for job_skill in job_skill_list:
        found = False

        for user_skill in user_skill_list:

            if user_skill in job_skill or job_skill in user_skill:
                found = True
                break

        if not found:
            missing.append(job_skill)

    return list(dict.fromkeys(missing))


# RECOMMENDATION BUTTON
if st.sidebar.button("Find Jobs", use_container_width=True):

    if not user_skills.strip() and not user_interests.strip():

        st.warning("Please enter at least your skills or interests.")

    else:

        # USER PROFILE
        user_profile = (
            user_skills + " " +
            user_interests
        ).lower()

        # TF-IDF
        vectorizer = TfidfVectorizer(stop_words="english")

        job_vectors = vectorizer.fit_transform(df["search_text"])

        user_vector = vectorizer.transform([user_profile])

        # COSINE SIMILARITY
        similarity_scores = cosine_similarity(
            user_vector,
            job_vectors
        )[0]

        df["similarity_score"] = similarity_scores


        # CATEGORY BONUS
        if user_category != "Any":

            category_match = (
                df["category"]
                .str.lower()
                .str.contains(
                    user_category.lower(),
                    na=False
                )
            )

            df.loc[
                category_match,
                "similarity_score"
            ] += 0.15

        # EXPERIENCE COMPATIBILITY
        df["required_experience"] = (
            df["job_description"]
            .fillna("")
            .apply(extract_experience)
        )

        def experience_bonus(required):

            if required == 0:
                return 0

            if experience >= required:
                return 0.10

            return -0.05


        df["experience_bonus"] = (
            df["required_experience"]
            .apply(experience_bonus)
        )

        df["final_score"] = (
            df["similarity_score"] +
            df["experience_bonus"]
        )

        # RANK JOBS
        recommendations = (
            df.sort_values(
                by="final_score",
                ascending=False
            )
            .head(num_recommendations)
        )

        # RESULTS
        st.subheader("Recommended Jobs")

        st.caption(
            f"Showing the top {num_recommendations} matches "
            f"from {len(df):,} job postings."
        )

        # SCORE CHART

        chart_data = recommendations[["job_title", "final_score"]].copy()

        chart_data["final_score"] = (
            chart_data["final_score"]
            .clip(0, 1)
        )

        chart_data = chart_data.set_index("job_title")

        st.subheader("Recommendation Scores")

        st.bar_chart(chart_data["final_score"])

        # JOB CARDS
        for _, row in recommendations.iterrows():
            score = max(0, min(row["final_score"], 1))

            matched_skills = get_matched_skills(user_skills, row["job_skill_set"])
            missing_skills = get_missing_skills(user_skills, row["job_skill_set"])

            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                # JOB INFORMATION
                with col1:
                    st.markdown(f"### {row['job_title']}")
                    st.write(
                        f"**Category:** "
                        f"{row['category']}")

                    if row["required_experience"] > 0:
                        st.write(
                            f"**Estimated Experience "
                            f"Required:** "
                            f"{row['required_experience']}+ years")
                    else:
                        st.write("**Experience:** " "Not specified")

                # MATCH SCORE
                with col2:
                    st.metric("Match Score",f"{score:.1%}")
                    st.progress(score)

                # SKILL MATCH
                st.markdown("**Matched Skills**")

                if matched_skills:
                    st.write(", ".join(matched_skills))
                else:
                    st.write("No direct skill matches found.")
                st.markdown("**Skills You May Need**")

                if missing_skills:
                    st.write(", ".join(missing_skills[:10]))
                else:
                    st.write("No major missing skills detected.")
                # ALL JOB SKILLS
                with st.expander("View Required Skills"):
                    st.write(", ".join(row["job_skill_set"]))
                # JOB DESCRIPTION
                with st.expander(
                    "View Job Description"):
                    st.write(row["job_description"])

else:

    # LANDING PAGE
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Available",f"{len(df):,}")

    with col2:
        st.metric("Categories",df["category"].nunique())

    with col3:
        st.metric("Recommendation", "TF-IDF + Cosine")

    st.divider()
    st.info(
        "Enter your skills, interests and experience "
        "in the sidebar to get personalized recommendations."
    )