# Heart Disease Classification using Supervised Machine Learning 

## Overview

This project implements a comparative supervised machine learning approach for heart disease classification.

The goal is to train and evaluate multiple classification algorithms and determine which model performs best based on standard classification metrics.

The project compares:

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Decision Tree

After comparing the models, the best-performing model is used to make predictions on new patient input data.

## Project Workflow

```text
Dataset
   ↓
Understand Data
   ↓
Exploratory Data Analysis
   ↓
Data Cleaning Checks
   ↓
Feature / Target Separation
   ↓
Train / Test Split
   ↓
Feature Scaling
   ↓
┌─────────────────────────────┐
│ Logistic Regression         │
│ KNN                         │
│ Decision Tree               │
└─────────────────────────────┘
   ↓
Model Evaluation
   ↓
Model Comparison
   ↓
Best Model Selection
   ↓
New Patient Prediction
```

## Dataset

The dataset contains patient-related features used to classify whether the target indicates the presence of heart disease.

The dataset contains **303 records and 14 columns**, including 13 input features and one target variable.

### Target

* `0` → No Disease
* `1` → Disease

## Exploratory Data Analysis

The project performs several EDA steps before model training:

* Dataset shape and information
* Descriptive statistics
* Missing-value analysis
* Duplicate-row analysis
* Target class distribution
* Numerical feature distributions
* Categorical feature distributions
* Feature correlation heatmap

## Data Preparation

The target column is separated from the input features:

```python
X = df.drop("target", axis=1)
y = df["target"]
```

The dataset is divided into training and testing sets using an 80/20 split with stratification to preserve the target-class distribution.

For Logistic Regression and KNN, `StandardScaler` is applied using only the training data before transforming the test data.

## Machine Learning Models

### 1. Logistic Regression

A Logistic Regression classifier is trained on the standardized features.

### 2. K-Nearest Neighbors

KNN is trained using standardized features with `n_neighbors=5`.

### 3. Decision Tree

A Decision Tree classifier is trained on the original feature values.

## Model Evaluation

Each model is evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

The models are compared using a Pandas DataFrame, and the model with the highest F1 Score is automatically selected as the best model.

## Results

The initial model comparison produced the following results:

| Model               | Accuracy | Precision | Recall |   F1 Score |
| ------------------- | -------: | --------: | -----: | ---------: |
| Logistic Regression |   88.52% |    87.88% | 90.63% | **89.23%** |
| KNN                 |   68.85% |    68.57% | 75.00% |     71.64% |
| Decision Tree       |   75.41% |    84.00% | 65.63% |     73.68% |

### Best Model

**Logistic Regression**

* Accuracy: 88.52%
* Precision: 87.88%
* Recall: 90.63%
* F1 Score: 89.23%

The model is selected automatically based on the highest F1 Score.

> Note: These results are based on a single train/test split and are intended for educational and internship-project purposes.

## New Patient Prediction

The project also accepts feature values for a new patient through command-line input.

The selected Logistic Regression model then provides:

* Predicted class
* Estimated probability of No Disease
* Estimated probability of Disease

Example:

```text
Prediction:
The model predicts: Disease

Probability of No Disease: 18.43%
Probability of Disease: 81.57%
```

These probabilities represent model estimates and should not be interpreted as a medical diagnosis.

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SymbolPamnani/Python-learning/tree/main/Mini_Projects
```

### 2. Navigate to the project directory

```bash
cd Heart-disease-detection
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the project

```bash
python heart_disease.py
```

The program will perform EDA, train the classification models, compare their performance, display confusion matrices, and ask for new patient data for prediction.

## Project Objective

This project demonstrates the practical implementation of supervised machine learning classification, including:

* Data exploration
* Data preparation
* Feature scaling
* Model training
* Model evaluation
* Comparative model analysis
* Model selection
* Prediction on new data

## Disclaimer

This project is developed for educational and machine learning practice purposes. It is not intended for medical diagnosis or clinical decision-making.
