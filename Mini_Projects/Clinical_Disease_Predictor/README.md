# Task 4 — High-Imbalance Clinical Disease Predictor Pipeline

## Project summary
This project compares SVM, Random Forest, and XGBoost models for predicting malignant vs benign breast tumors. It demonstrates SMOTE resampling, class weighting, stratified 5-fold cross-validation, and recall-focused evaluation.

## Dataset note
The code uses scikit-learn's built-in Breast Cancer Wisconsin Diagnostic dataset, so no separate CSV download is required. It has 569 samples and 30 numerical features. Its class distribution is not extremely imbalanced; the project demonstrates imbalance-handling methods, but do not describe this particular dataset as severely imbalanced in the report.

## Pipeline
1. Load data and inspect class counts.
2. Create a stratified train/test split.
3. Apply SMOTE only inside training folds via imbalanced-learn pipelines to avoid data leakage.
4. Train SVM, Random Forest, and XGBoost (if installed).
5. Evaluate with stratified 5-fold CV.
6. Compare recall, precision, F1-score, accuracy, and ROC-AUC.
7. Save classification reports, confusion matrices, comparison CSVs, and the CV-selected model.

## Install (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python task4_disease_predictor.py
```

If activation is blocked:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe task4_disease_predictor.py
```

## Output files
- `results/dataset_overview.csv`
- `results/cross_validation_results.csv`
- `results/test_model_comparison.csv`
- `results/*_classification_report.csv`
- `results/selected_model.txt`
- `results/plots/class_distribution.png`
- `results/plots/*_confusion_matrix.png`
- `results/plots/recall_comparison.png`
- `models/best_recall_cv_model.joblib`

## Important
This is an educational machine-learning exercise, not a medical diagnostic tool. Results are not suitable for clinical decisions. The final model choice should consider recall and false negatives alongside precision and validation performance.
