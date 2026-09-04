# AI Job Recommendation System

An AI/ML-powered job recommendation system that recommends relevant job opportunities based on a user's **skills, interests, preferred category, and experience**.

The system uses **TF-IDF vectorization and Cosine Similarity** to compare the user's profile with real job-posting data and rank the most relevant opportunities.

## Features

* Personalized job recommendations
* TF-IDF based text representation
* Cosine Similarity for job matching
* Skill-based recommendation
* Matched skills identification
* Missing skills identification
* Preferred job category filtering
* Experience compatibility analysis
* Recommendation score visualization
* Interactive Streamlit interface
* Expandable job descriptions
* Job skill analysis

## How It Works

```text
User Skills
     +
User Interests
     +
Experience
     +
Preferred Category
        ↓
   User Profile
        ↓
   TF-IDF Vectorization
        ↓
   Cosine Similarity
        ↓
 Category Matching
        ↓
Experience Compatibility
        ↓
    Final Score
        ↓
 Ranked Job Recommendations
```

## Technologies

* Python
* Pandas
* Scikit-learn
* Streamlit
* TF-IDF
* Cosine Similarity
* Regex

## Dataset

The system uses a dataset containing job postings with information including:

* Job ID
* Job Category
* Job Title
* Job Description
* Required Skill Set

## Run Locally

Clone the repository:

```bash
git clone https://github.com/SymbolPamnani/Python-learning/tree/main/Mini_Projects
```

Navigate to the project:

```bash
cd Jobs-Recommendation-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run jobs_recommendation.py
```

## Example

A user can enter:

```text
Skills:
Python, SQL, AWS, Git, Machine Learning

Interests:
Artificial Intelligence, Data Science

Experience:
1 year
```

The system then ranks jobs according to how closely their requirements match the user's profile.

## Project Goal

The goal of this project is to demonstrate how **text-based machine learning techniques** can be applied to build a practical recommendation system.

Rather than using a simple keyword search, the system represents job information and the user's profile as TF-IDF vectors and calculates their similarity using cosine similarity.

## Future Improvements

* Semantic embeddings using transformer models
* More advanced skill extraction
* Experience-level classification
* Personalized learning recommendations for missing skills
* Resume upload and automatic skill extraction
* Job recommendation history
* Deployment as a public web application

## Author

**Symbol Pamnani**

BS Computer Science | AI/ML Enthusiast