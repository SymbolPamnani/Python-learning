import streamlit as st
import easyocr
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# -------------------
# Page Configuration
# -------------------

st.set_page_config(
    page_title="AI Text Recognition",
    layout="wide"
)

# ----------
# Title
# ----------

st.title("AI Image Text Recognition")

st.write(
    "Upload an image and use AI-powered OCR to extract, "
    "analyze, and understand the text."
)


# -------------------
# Load OCR Model
# -------------------

@st.cache_resource
def load_model():

    reader = easyocr.Reader(
        ["en"],
        gpu=False
    )

    return reader


reader = load_model()

# -------------------
# Helper Functions
# -------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_keywords(text, number=10):

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=number
    )

    try:

        vectorizer.fit_transform([cleaned_text])

        keywords = vectorizer.get_feature_names_out()

        return list(keywords)

    except ValueError:

        return []


def classify_document(text):

    text = text.lower()

    categories = {

        "Resume / CV": [
            "resume",
            "cv",
            "experience",
            "education",
            "skills",
            "employment",
            "linkedin",
            "projects"
        ],

        "Certificate": [
            "certificate",
            "certification",
            "certified",
            "achievement",
            "completion",
            "awarded"
        ],

        "Academic": [
            "university",
            "college",
            "student",
            "course",
            "assignment",
            "semester",
            "research",
            "academic"
        ],

        "Business": [
            "company",
            "business",
            "manager",
            "employee",
            "organization",
            "sales",
            "revenue"
        ],

        "Technical": [
            "python",
            "programming",
            "software",
            "machine learning",
            "artificial intelligence",
            "database",
            "developer",
            "algorithm"
        ]
    }

    scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:

        return "General Document"

    return best_category


# -------------------
# Image Upload
# -------------------

uploaded_file = st.file_uploader(
    "Upload an image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# -------------------
# Recognition
# -------------------

if uploaded_file:

    image = Image.open(uploaded_file)

    st.subheader("Uploaded Image")

    st.image(
        image,
        caption="Input Image",
    )


    if st.button(
        "Extract & Analyze Text",
        use_container_width=True
    ):

        with st.spinner(
            "AI is recognizing the text..."
        ):

            results = reader.readtext(
                uploaded_file.getvalue()
            )


        # -------------------
        # Check Results
        # -------------------

        if results:

            extracted_text = []

            confidence_scores = []


            # -------------------
            # OCR Results
            # -------------------

            st.subheader("Recognized Text")

            for detection in results:

                text = detection[1]

                confidence = detection[2]

                extracted_text.append(text)

                confidence_scores.append(
                    confidence
                )

                st.write(
                    f"**{text}** "
                    f"— Confidence: "
                    f"{confidence:.2%}"
                )


            # -------------------
            # Complete Text
            # -------------------

            complete_text = " ".join(
                extracted_text
            )


            st.divider()

            st.subheader(
                "Document Analysis"
            )


            # -------------------
            # Statistics
            # -------------------

            word_count = len(
                complete_text.split()
            )

            character_count = len(
                complete_text
            )

            text_region_count = len(
                results
            )

            average_confidence = (
                sum(confidence_scores)
                / len(confidence_scores)
            )


            # -------------------
            # Statistics Cards
            # -------------------

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Words",
                    word_count
                )

            with col2:

                st.metric(
                    "Characters",
                    character_count
                )

            with col3:

                st.metric(
                    "Text Regions",
                    text_region_count
                )

            with col4:

                st.metric(
                    "Avg Confidence",
                    f"{average_confidence:.2%}"
                )


            # -------------------
            # Document Category
            # -------------------

            category = classify_document(
                complete_text
            )

            st.subheader(
                "Document Category"
            )

            st.success(
                f"Detected Category: **{category}**"
            )


            # -------------------
            # Keywords
            # -------------------

            st.subheader(
                "Extracted Keywords"
            )

            keywords = extract_keywords(
                complete_text
            )

            if keywords:

                st.write(
                    " • ".join(keywords)
                )

            else:

                st.info(
                    "Not enough text to extract keywords."
                )


            # -------------------
            # Complete Text
            # -------------------

            st.subheader(
                "Complete Extracted Text"
            )

            st.text_area(
                "Extracted Text",
                complete_text,
                height=250
            )


            # -------------------
            # Download Text
            # -------------------

            st.download_button(
                label="Download Extracted Text",
                data=complete_text,
                file_name="extracted_text.txt",
                mime="text/plain",
                use_container_width=True
            )


        else:

            st.warning(
                "No text was detected in the image."
            )


else:

    st.info(
        "Upload an image containing text "
        "to begin recognition."
    )