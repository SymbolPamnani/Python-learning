import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "customer_churn.csv"
MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.txt"

# Load Dataset
df = pd.read_csv(DATA_PATH)

# Separate Features and Target
y = df["Churn"]
X = df.drop(columns=["Churn"])

# Remove irrelevant and leakage features
X = X.drop(columns=["Customer_ID", "Cancellation_Date"])

# Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Feature Types
numerical_features = [
    "Age",
    "Tenure_Months",
    "Monthly_Charges",
    "Total_Charges",
    "Support_Calls",
    "Payment_Delays",
    "Num_Products"
]

categorical_features = [
    "Contract_Length",
    "Has_Internet",
    "Has_Streaming",
    "Gender"
]


# Preprocessing Pipelines
numerical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)


# Combine Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numerical_transformer,
            numerical_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)


# Final Logistic Regression Model
model = Pipeline(steps=[("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])

# Threshold selection using cross-validation 
print("\n---------------------------------------")
print("THRESHOLD SELECTION")
print("---------------------------------------")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("\nGenerating out-of-fold probabilities...")

oof_probabilities = cross_val_predict(model, X_train, y_train, cv=cv, method="predict_proba")[:, 1]

print("Out-of-fold probabilities generated successfully.")

# Test different thresholds
thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]

threshold_results = []

print("\nThreshold Analysis:")

for threshold in thresholds:

    predictions = (oof_probabilities >= threshold).astype(int)
    precision = precision_score(y_train, predictions, zero_division=0)
    recall = recall_score(y_train, predictions, zero_division=0)
    f1 = f1_score(y_train, predictions, zero_division=0)

    threshold_results.append({
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    })

    print(
        f"Threshold: {threshold:.2f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f}"
    )

# Select threshold with best F1
best_threshold_result = max(threshold_results, key=lambda result: result["F1"])

best_threshold = best_threshold_result["Threshold"]

print("\n---------------------------------------")
print("BEST THRESHOLD")
print("---------------------------------------")

print("Best Threshold:", best_threshold)
print("Precision:", round(best_threshold_result["Precision"], 3))
print("Recall:", round(best_threshold_result["Recall"], 3))
print("F1 Score:", round(best_threshold_result["F1"], 3))

# Train final model
print("\n--------------------------")
print("FINAL MODEL TRAINING")
print("----------------------------")

print("\nTraining Logistic Regression model...")
model.fit(X_train, y_train)
print("Model trained successfully.")

# FINAL TEST EVALUATION
print("\n---------------------------------------")
print("FINAL TEST SET EVALUATION")
print("---------------------------------------")

# Get probability instead of using default 0.50
test_probabilities = model.predict_proba(X_test)[:, 1]

# Apply selected threshold
test_predictions = (test_probabilities >= best_threshold).astype(int)

test_precision = precision_score(y_test, test_predictions, zero_division=0)
test_recall = recall_score(y_test, test_predictions, zero_division=0)
test_f1 = f1_score(y_test, test_predictions, zero_division=0)

print("Threshold:", best_threshold)
print("Test Precision:", round(test_precision, 3))
print("Test Recall:", round(test_recall, 3))
print("Test F1:", round(test_f1, 3))


# Save model
model_path = MODEL_PATH

joblib.dump(model, model_path)

print(f"\nModel saved to: {model_path}")


# Save threshold
threshold_path = THRESHOLD_PATH

with open(threshold_path, "w") as file:
    file.write(str(best_threshold))

print(f"Threshold saved to: {threshold_path}")