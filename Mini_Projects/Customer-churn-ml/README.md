# Customer Churn Prediction

A machine learning project that predicts whether a customer is likely to churn based on customer demographics, usage, billing, and service-related information.

The project focuses on the complete machine learning workflow, including data exploration, preprocessing, model comparison, class imbalance handling, threshold optimization, model evaluation, and deployment through a Streamlit application.

---

## Project Objective

Customer churn occurs when a customer stops using a company's products or services.

The goal of this project is to build a binary classification model that predicts:

- `0` → Customer is likely to stay
- `1` → Customer is likely to churn

Because churned customers represent a minority of the dataset, accuracy alone is not sufficient for evaluating the model. Precision, recall, and F1 score are also considered.

---

## Dataset

The dataset contains 1,000 customer records.

### Features

- Age
- Tenure_Months
- Monthly_Charges
- Total_Charges
- Support_Calls
- Payment_Delays
- Num_Products
- Contract_Length
- Has_Internet
- Has_Streaming
- Gender

### Target

- `Churn`

The dataset contains:

- 849 non-churned customers
- 151 churned customers

This means approximately 15.1% of customers in the dataset are churners.

---


## Machine Learning Workflow

Dataset
   ↓
Exploratory Data Analysis
   ↓
Leakage Detection
   ↓
Train/Test Split
   ↓
Missing Value Handling
   ↓
Feature Scaling
   ↓
Categorical Encoding
   ↓
Logistic Regression Baseline
   ↓
Cross-Validation
   ↓
Class Imbalance Handling
   ↓
Decision Tree Experimentation
   ↓
Threshold Optimization
   ↓
Final Logistic Regression Model
   ↓
Test Evaluation
   ↓
Model Serialization
   ↓
Streamlit Application

## Running the Project

Clone the repository and navigate into the project directory.

1. Install the dependencies:

pip install -r requirements.txt

2. Run the prediction script:

python src/predict.py

3. Run the Streamlit application:

streamlit run app.py

### Technologies Used
Python
Pandas
Scikit-learn
Joblib
Streamlit

## Key Concepts Practiced
Exploratory Data Analysis
Missing Value Imputation
Feature Scaling
One-Hot Encoding
ColumnTransformer
Machine Learning Pipelines
Logistic Regression
Decision Trees
Stratified Train/Test Split
Stratified K-Fold Cross-Validation
Class Imbalance
Precision
Recall
F1 Score
Confusion Matrix
Decision Threshold Optimization
Out-of-Fold Predictions
Model Serialization
Streamlit Deployment

## Project Structure

```text
Customer-churn-ml/
│
├── Data/
│   └── customer_churn.csv
│
├── models/
│   ├── churn_model.pkl
│   └── threshold.txt
│
├── src/
│   ├── preprocessing.py
│   ├── model_training.py
│   └── predict.py
│
├── app.py
├── concepts.txt
├── requirements.txt
└── README.md