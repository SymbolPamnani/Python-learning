# AI Image Text Recognition & Document Analysis

An AI-powered image text recognition application built with Python and Streamlit. The application uses EasyOCR to extract text from images and performs additional text analysis using TF-IDF.

## Features

- Extract text from images using AI-powered OCR
- Display individual detected text regions
- Display confidence scores for detected text
- Calculate total word count
- Calculate total character count
- Count detected text regions
- Calculate average OCR confidence
- Extract important keywords using TF-IDF
- Detect basic document categories
- Display complete extracted text
- Download extracted text as a `.txt` file
- Interactive Streamlit user interface

## Technologies Used

- Python
- Streamlit
- EasyOCR
- Scikit-learn
- Pandas
- Pillow
- Regular Expressions (Regex)

## AI and Machine Learning Techniques

### Optical Character Recognition

EasyOCR is used to detect and recognize text present inside uploaded images.

The OCR model returns the detected text along with a confidence score for each detected text region.

### TF-IDF

Term Frequency-Inverse Document Frequency (TF-IDF) is used to identify important keywords from the extracted text.

The extracted text is cleaned and processed before TF-IDF is applied.

### Document Category Detection

The application performs basic document categorization based on keywords found in the extracted text.

The current categories include:

- Resume / CV
- Certificate
- Academic
- Business
- Technical
- General Document

## Installation

1. Clone the Repository
git clone <your-repository-url>

2. Navigate to the Project Directory
cd Python-learning/Mini_Projects/AI-Image-Text-Recognition

3. Create a Virtual Environment
python -m venv venv

4. Activate the Virtual Environment
Windows: venv\Scripts\activate
macOS / Linux: source venv/bin/activate

5. Install Dependencies
pip install -r requirements.txt

## Run the Application

streamlit run text_recognition.py


## Usage
Start the application using the Streamlit command.
Upload an image containing readable text.
Click Extract & Analyze Text.
EasyOCR processes the uploaded image.
View the recognized text and confidence scores.
View document statistics.
View extracted keywords using TF-IDF.
View the detected document category.
Download the complete extracted text as a .txt file.

### Supported Input Formats

The application currently supports:

JPG
JPEG
PNG

### Output
The application provides the following information:

1. Recognized Text

2. Displays each detected text region separately along with its OCR confidence score.

3. Document Statistics

4. The application calculates:

Total words
Total characters
Number of detected text regions
Average OCR confidence

5. Extracted Keywords

TF-IDF is used to identify relevant keywords from the extracted text.

6. Document Category

The application provides a basic category prediction based on keywords detected in the extracted text.

7. Downloadable Text

The complete extracted text can be downloaded as a .txt file.

## Project Structure
AI-Image-Text-Recognition/
│
├── text_recognition.py
├── requirements.txt
└── README.md

## Requirements

The project dependencies are listed in requirements.txt.

Example:

streamlit
easyocr
Pillow
scikit-learn
pandas

## Future Improvements

Possible future improvements include:

Support for multiple languages
PDF document support
Batch image processing
Improved document classification using a trained machine learning model
Named Entity Recognition
Sentiment analysis
Advanced text preprocessing
Improved OCR accuracy
Cloud deployment
Database integration
History of previously processed documents

## Learning Objectives

This project was developed as part of my Python and AI/ML learning journey.

The project provides practical experience with:

Python programming
Artificial Intelligence
Optical Character Recognition
Natural Language Processing
TF-IDF
Text preprocessing
Machine learning concepts
Streamlit application development
Building practical AI applications
License

This project is created for educational and learning purposes.

## How It Works

```text
                    Upload Image
                         |
                         v
                      EasyOCR
                         |
                         v
                   Extract Text
                         |
              +----------+----------+
              |                     |
              v                     v
       Confidence Scores       Text Analysis
                                    |
                    +---------------+---------------+
                    |               |               |
                    v               v               v
                Statistics       TF-IDF         Category
                                 Keywords       Detection
                    |               |               |
                    +---------------+---------------+
                                    |
                                    v
                             Display Results
                                    |
                                    v
                            Download Text

## License

This project is created for educational and learning purposes.