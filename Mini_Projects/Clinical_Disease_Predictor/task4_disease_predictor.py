"""
Progree Internship - Task 4
Clinical Disease Predictor Pipeline with Imbalance Handling

Dataset: Breast Cancer Wisconsin Diagnostic dataset from scikit-learn.
Models: SVM, Random Forest, and XGBoost (if installed).
Techniques: SMOTE, class weighting, stratified cross-validation, recall-focused evaluation.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline as SklearnPipeline
from sklearn.metrics import (
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

warnings.filterwarnings("ignore")

SEED = 42
RESULTS = "results"
PLOTS = os.path.join(RESULTS, "plots")
os.makedirs(PLOTS, exist_ok=True)

# 1. Load built-in Breast Cancer Wisconsin Diagnostic dataset
dataset = load_breast_cancer(as_frame=True)
X = dataset.data.copy()
# scikit-learn target: 0=malignant, 1=benign. Re-map positive class to malignant=1
y = (dataset.target == 0).astype(int)
class_names = ["Benign", "Malignant"]

print("Dataset shape:", X.shape)
print("Target distribution (0=Benign, 1=Malignant):")
print(pd.Series(y).value_counts().sort_index().rename(index={0: "Benign", 1: "Malignant"}))

# Save dataset overview
overview = pd.DataFrame({
    "feature": X.columns,
    "missing_values": X.isna().sum().values,
    "mean": X.mean().values,
    "std": X.std().values
})
overview.to_csv(os.path.join(RESULTS, "dataset_overview.csv"), index=False)

# Plot class distribution
counts = pd.Series(y).value_counts().sort_index()
plt.figure(figsize=(6, 4))
plt.bar(["Benign", "Malignant"], [counts.get(0, 0), counts.get(1, 0)])
plt.title("Breast Cancer Dataset Class Distribution")
plt.xlabel("Class")
plt.ylabel("Number of samples")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "class_distribution.png"), dpi=250)
plt.close()

# 2. Stratified train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)

# 3. Define models with imbalance handling
models = {
    "SVM_SMOTE": ImbPipeline([
        ("scaler", StandardScaler()),
        ("smote", SMOTE(random_state=SEED)),
        ("model", SVC(kernel="rbf", class_weight="balanced", probability=True,
                      random_state=SEED))
    ]),
    "RandomForest_SMOTE": ImbPipeline([
        ("smote", SMOTE(random_state=SEED)),
        ("model", RandomForestClassifier(
            n_estimators=300, class_weight="balanced",
            random_state=SEED, n_jobs=-1
        ))
    ]),
}

# XGBoost is optional, with a clear message if the package is missing.
try:
    from xgboost import XGBClassifier
    # scale_pos_weight is calculated from the training split; SMOTE is also applied
    negative_count = int((y_train == 0).sum())
    positive_count = int((y_train == 1).sum())
    models["XGBoost_SMOTE"] = ImbPipeline([
        ("smote", SMOTE(random_state=SEED)),
        ("model", XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            scale_pos_weight=max(negative_count, positive_count) / max(1, min(negative_count, positive_count)),
            eval_metric="logloss",
            random_state=SEED,
            n_jobs=-1
        ))
    ])
except ImportError:
    print("xgboost is not installed; XGBoost will be skipped. Install requirements.txt to enable it.")

# 4. Recall-focused cross-validation on training data
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1",
    "roc_auc": "roc_auc"
}
cv_rows = []
test_rows = []
fitted_models = {}
predictions_by_model = {}

for name, estimator in models.items():
    print(f"\nCross-validating {name}...")
    cv_results = cross_validate(
        estimator, X_train, y_train, cv=cv, scoring=scoring,
        n_jobs=1, return_train_score=False
    )
    cv_rows.append({
        "model": name,
        "cv_accuracy_mean": cv_results["test_accuracy"].mean(),
        "cv_accuracy_std": cv_results["test_accuracy"].std(),
        "cv_precision_mean": cv_results["test_precision"].mean(),
        "cv_recall_mean": cv_results["test_recall"].mean(),
        "cv_f1_mean": cv_results["test_f1"].mean(),
        "cv_roc_auc_mean": cv_results["test_roc_auc"].mean()
    })

    print("Fitting final model...")
    estimator.fit(X_train, y_train)
    y_pred = estimator.predict(X_test)
    y_prob = estimator.predict_proba(X_test)[:, 1]
    fitted_models[name] = estimator
    predictions_by_model[name] = (y_pred, y_prob)

    test_rows.append({
        "model": name,
        "test_accuracy": accuracy_score(y_test, y_pred),
        "test_precision": precision_score(y_test, y_pred, zero_division=0),
        "test_recall": recall_score(y_test, y_pred, zero_division=0),
        "test_f1": f1_score(y_test, y_pred, zero_division=0),
        "test_roc_auc": roc_auc_score(y_test, y_prob)
    })

    # Per-model report and confusion matrix
    report = classification_report(
        y_test, y_pred, labels=[0, 1], target_names=class_names,
        output_dict=True, zero_division=0
    )
    pd.DataFrame(report).transpose().to_csv(
        os.path.join(RESULTS, f"{name.lower()}_classification_report.csv")
    )

    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay(cm, display_labels=class_names).plot(
        ax=ax, values_format="d", cmap="Blues"
    )
    ax.set_title(f"{name} - Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS, f"{name.lower()}_confusion_matrix.png"), dpi=250)
    plt.close()

# 5. Save comparison tables
cv_df = pd.DataFrame(cv_rows).sort_values("cv_recall_mean", ascending=False)
test_df = pd.DataFrame(test_rows).sort_values("test_recall", ascending=False)
cv_df.to_csv(os.path.join(RESULTS, "cross_validation_results.csv"), index=False)
test_df.to_csv(os.path.join(RESULTS, "test_model_comparison.csv"), index=False)

print("\nCross-validation comparison (sorted by mean recall):")
print(cv_df.to_string(index=False))
print("\nHeld-out test comparison (sorted by recall):")
print(test_df.to_string(index=False))

# 6. Plot test recall comparison
plt.figure(figsize=(8, 5))
plt.bar(test_df["model"], test_df["test_recall"])
plt.title("Test Recall Comparison")
plt.ylabel("Recall for malignant class")
plt.ylim(0, 1.05)
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "recall_comparison.png"), dpi=250)
plt.close()

# 7. Save best recall model (best on test recall is reported for comparison only;
# selection for a final deployment should be based on validation CV, not test data).
best_name = cv_df.iloc[0]["model"]
best_model = fitted_models[best_name]
import joblib
joblib.dump(best_model, os.path.join("models", "best_recall_cv_model.joblib"))
with open(os.path.join(RESULTS, "selected_model.txt"), "w", encoding="utf-8") as f:
    f.write(f"Selected by highest mean 5-fold CV recall: {best_name}\n")
    f.write("Check recall, precision, ROC-AUC, and false negatives before drawing conclusions.\n")

print(f"\nSaved CV-selected model: {best_name}")
print("Task 4 complete. Review results/ and results/plots/.")
