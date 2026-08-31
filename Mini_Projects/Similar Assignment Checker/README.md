Assignment Similarity Checker

An NLP-based web application that compares multiple student assignments and identifies potentially similar submissions using TF-IDF and Cosine Similarity. The application is built with Python and Streamlit and supports both TXT and PDF assignments.

Features
Upload multiple TXT or PDF assignments
Extract text from uploaded files
Preprocess text using lowercase conversion, punctuation removal, and stopword removal
Convert assignments into TF-IDF vectors
Calculate pairwise Cosine Similarity
Find the most similar assignment for each student
Set a custom similarity threshold
Identify potentially similar assignment pairs
Display a complete similarity matrix
Visualize similarity scores using Matplotlib
Download similarity results as a CSV file
Technologies Used
Python
Streamlit
Pandas
Matplotlib
Scikit-learn
NLTK
PyPDF
How It Works
Student Assignments
        |
        v
Text Extraction
        |
        v
Text Preprocessing
        |
        v
TF-IDF Vectorization
        |
        v
Cosine Similarity
        |
        v
Similarity Scores
        |
        +-------------------+
        |                   |
        v                   v
Similarity Matrix     Similar Assignment Pairs
        |
        v
Visualization and Results
TF-IDF

TF-IDF (Term Frequency-Inverse Document Frequency) converts text into numerical vectors based on the importance of words within the assignments.

Cosine Similarity

Cosine Similarity measures the similarity between the TF-IDF vectors of two assignments. The resulting value is converted into a percentage for easier interpretation.

A higher percentage indicates greater textual similarity.

Installation

Clone the repository:

git clone https://github.com/SymbolPamnani/Mini_Projects/Similar Assignment Checker

Navigate to the project directory:

cd assignment-similarity-checker

Install the required libraries:

pip install streamlit pandas matplotlib scikit-learn nltk pypdf
Run the Application
streamlit run assignment_checker.py

The application will open in your browser.

Usage
Upload two or more TXT or PDF assignments.
Select a similarity threshold.
The application extracts and preprocesses the assignment text.
TF-IDF converts the assignments into numerical representations.
Cosine Similarity compares the assignments.
Review the similarity scores and similarity matrix.
Check the potentially similar assignment pairs.
Download the results as a CSV file.
Project Structure
similar-assignment-checker/
│
├── assignment_checker.py
├── README.md
└── requirements.txt
Important Note

This project detects textual similarity between assignments. A high similarity score does not necessarily prove plagiarism because students may use common terminology, references, templates, or required content. The results should therefore be used as an indicator for further review rather than as a final plagiarism decision.

Future Improvements
Add DOCX support
Improve text preprocessing
Add semantic similarity using embeddings
Add student name extraction
Add downloadable similarity reports
Add a more detailed dashboard
Add highlighting of similar text sections
Store and compare assignments using a database
Learning Objectives

This project was developed to gain practical experience with NLP, TF-IDF, Cosine Similarity, text preprocessing, file handling, data visualization, and Streamlit application development.