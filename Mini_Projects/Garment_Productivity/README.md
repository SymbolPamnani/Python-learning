# Task 2: Garment Worker Productivity Prediction & Modeling

A machine learning project designed to analyze and predict the actual productivity of garment workers using regression techniques, detailed exploratory data analysis (EDA), hyperparameter tuning, and cross-validation.

---

## 📌 Project Overview

This repository contains a full predictive workflow using the **Garment Worker Productivity Dataset**. The primary goal is to model productivity drivers, evaluate linear baseline models, and optimize regularized regression methods to understand key features influencing factory output.

### Key Enhancements Included:
- **Exploratory Data Analysis (EDA):** Visualizations for target distribution, missing values, correlation structures, and departmental performance.
- **Data Preprocessing Pipeline:** Integrated missing-value imputation (`SimpleImputer`), numeric feature scaling (`StandardScaler`), and categorical encoding (`OneHotEncoder`).
- **Baseline Benchmarking:** Comparison between a Dummy Mean Baseline, Ordinary Least Squares (OLS) Linear Regression, and Ridge Regression.
- **Hyperparameter Tuning:** 5-fold cross-validation (`RidgeCV`) across 50 $\alpha$ values to optimize L2 regularization.
- **Model Evaluation & Residual Analysis:** Full metric logging ($R^2$, $\text{RMSE}$, $\text{MAE}$) along with residual distribution analysis.
- **Feature Importance:** Automated extraction and export of regression coefficients to rank feature impact.

---

## 📊 Pipeline Overview
1. Preprocessing:
Strips whitespace and standardizes text strings in categorical features (e.g., department).
Handles missing values in numerical features (like wip) using mean imputation.
Applies StandardScaler to numerical columns and OneHotEncoder to categorical variables.
2. Model Training & Evaluation:
Evaluates a Mean Baseline Regressor as a ground-truth metric floor.
Fits an OLS Linear Regression model.
Performs a grid search over $\alpha \in [10^{-3}, 10^3]$ using RidgeCV with 5-fold cross-validation to select the optimal regularization penalty.
Logs overall 5-fold cross-validated $R^2$ scores to ensure model stability across splits.
3. Output Generation:
Saves predicted output against actual ground truth.
Visualizes residual behavior to inspect heteroscedasticity or systematic error patterns.
Outputs coefficient magnitudes to identify top positive and negative predictors of productivity.

## 🛠️ Setup & Usage
1. Requirements
Ensure you have Python 3.8+ installed. Install the required libraries via pip:

Bash
pip install -r requirements.txt
Key Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn

2. Execution
Run the main pipeline script from the project root:

Bash
python task2_linear_regression.py
All plots will be automatically generated and saved to results/plots/, and evaluation tables will be generated in results/.

## 📁 Repository Structure

```text
Task_2_Garment_Productivity/
├── data/
│   └── garments_worker_productivity.csv   # Source dataset
├── results/
│   ├── evaluation_metrics.csv             # Primary evaluation metrics
│   ├── model_comparison.csv               # Performance comparison across models
│   ├── predictions.csv                    # Actual vs Predicted values on test set
│   ├── feature_coefficients.csv           # Model coefficient rankings
│   └── plots/
│       ├── target_distribution.png        # Target variable histogram & KDE
│       ├── missing_values.png             # Missing data heatmap
│       ├── correlation_heatmap.png        # Feature correlation matrix
│       ├── productivity_by_department.png # Productivity breakdown across departments
│       └── residual_analysis.png          # Actual vs Predicted & residual distribution
├── task2_linear_regression.py            # Main execution pipeline
├── requirements.txt                       # Project dependencies
└── README.md                              # Project documentation