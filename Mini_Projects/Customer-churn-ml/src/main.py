import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import make_scorer

# Load Dataset
df = pd.read_csv("Python-learning/Mini_Projects/Customer-churn-ml/Data/customer_churn.csv")

print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nDataset information:")
print(df.info())

print("\nStatistical summary:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

print("\nChurn value counts:")
print(df["Churn"].value_counts())

print("\nChurn proportions:")
print(df["Churn"].value_counts(normalize=True))

print("\nData types:")
print(df.dtypes)

print("\nCancellation Date by Churn:")
print(df.groupby("Churn")["Cancellation_Date"].count())


# Train / Test Split
y = df["Churn"]
X = df.drop(columns=["Churn"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Remove irrelevant and leakage features
X_train = X_train.drop(columns=["Customer_ID", "Cancellation_Date"])
X_test = X_test.drop(columns=["Customer_ID", "Cancellation_Date"])

print("\nFinal training features:")
print(X_train.columns)
print("\nFinal testing features:")
print(X_test.columns)

# Features types
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

print("\nNumerical features:")
print(numerical_features)
print("\nCategorical features:")
print(categorical_features)


# Preprocessing pipelines
numerical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())])

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))])

preprocessor = ColumnTransformer(
    transformers=[("num", numerical_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features)])

# Logistic Regression baseline

print("----------------------------")
print("\nLOGISTIC REGRESSION BASELINE")
print("----------------------------")

logistic_model = Pipeline(
    steps=[("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])

logistic_model.fit(X_train, y_train)

logistic_predictions = logistic_model.predict(X_test)

print("\nTest Performance:")

print("Accuracy:", accuracy_score(y_test, logistic_predictions))
print("Precision:", precision_score(y_test, logistic_predictions, zero_division=0))
print("Recall:", recall_score( y_test, logistic_predictions, zero_division=0))
print("F1 Score:",f1_score(y_test, logistic_predictions, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix( y_test, logistic_predictions))

# Cross Validation 
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoring = {
    "accuracy": "accuracy",
    "precision": make_scorer(precision_score, zero_division=0),
    "recall": make_scorer(recall_score, zero_division=0),
    "f1": make_scorer(f1_score, zero_division=0)
}

# Logistic Regression Cross-validation

print("-------------------------------------")
print("\nLOGISTIC REGRESSION CROSS-VALIDATION")
print("-------------------------------------")

logistic_cv_results = cross_validate(logistic_model, X_train, y_train, cv=cv, scoring=scoring)

print("Mean Accuracy:", logistic_cv_results["test_accuracy"].mean())
print("Mean Precision:", logistic_cv_results["test_precision"].mean())
print("Mean Recall:", logistic_cv_results["test_recall"].mean())
print("Mean F1:", logistic_cv_results["test_f1"].mean())

# Decision Tree depth experiment
print("--------------------------------")
print("\nDECISION TREE DEPTH EXPERIMENT")
print("--------------------------------")

depths = [1, 2, 3, 4, 5, 7, 10, None]

depth_results = []

for depth in depths:
    tree_model = Pipeline(steps=[("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(
            max_depth=depth,
            class_weight="balanced",
            random_state=42
        ))])

    results = cross_validate(tree_model, X_train, y_train, cv=cv, scoring=scoring, return_train_score=True)

    depth_results.append({
            "Depth": depth,
            "Train Accuracy": results["train_accuracy"].mean(),
            "Validation Accuracy": results["test_accuracy"].mean(),
            "Train Precision": results["train_precision"].mean(),
            "Validation Precision": results["test_precision"].mean(),
            "Train Recall": results["train_recall"].mean(),
            "Validation Recall": results["test_recall"].mean(),
            "Train F1": results["train_f1"].mean(),
            "Validation F1": results["test_f1"].mean()})

# Display depth results
for result in depth_results:
    print("\nDepth:", result["Depth"])
    print("Train Accuracy:", round(result["Train Accuracy"], 3))
    print("Validation Accuracy:", round(result["Validation Accuracy"], 3))
    print("Train Precision:", round(result["Train Precision"], 3))
    print("Validation Precision:", round(result["Validation Precision"], 3))
    print("Train Recall:", round(result["Train Recall"], 3))
    print("Validation Recall:", round(result["Validation Recall"], 3))
    print("Train F1:", round(result["Train F1"], 3))
    print("Validation F1:", round(result["Validation F1"], 3))

#Selecting best depth
print("-----------------------------------")
print("\nBEST DEPTH BASED ON VALIDATION F1")
print("-----------------------------------")

best_depth_result = max(depth_results, key=lambda result: result["Validation F1"])
best_depth = best_depth_result["Depth"]
print("Best Depth:", best_depth)
print("Best Validation F1:", round(best_depth_result["Validation F1"],3))
print("Validation Recall:", round(best_depth_result["Validation Recall"], 3))
print("Validation Precision:", round(best_depth_result["Validation Precision"], 3))
print("Validation Accuracy:", round(best_depth_result["Validation Accuracy"], 3))

# Train final decision tree
print("-----------------------")
print("\nFINAL DECISION TREE")
print("-----------------------")

best_tree_model = Pipeline(steps=[("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(
            max_depth=best_depth,
            class_weight="balanced",
            random_state=42
        ))])

best_tree_model.fit(X_train, y_train)
print("Best tree model trained successfully.")

# Training performance
print("--------------------------")
print("\nTRAINING SET PERFORMANCE")
print("--------------------------")

train_predictions = best_tree_model.predict(X_train)

print("Training Accuracy:", accuracy_score(y_train, train_predictions))
print("Training Precision:", precision_score(y_train, train_predictions, zero_division=0))
print("Training Recall:", recall_score(y_train, train_predictions, zero_division=0))
print("Training F1:", f1_score(y_train, train_predictions, zero_division=0))

# Final test Performance
print("----------------------------")
print("\nFINAL TEST SET PERFORMANCE")
print("----------------------------")

test_predictions = best_tree_model.predict(X_test)

print("Test Accuracy:", accuracy_score(y_test, test_predictions))
print("Test Precision:", precision_score(y_test, test_predictions, zero_division=0))
print("Test Recall:",recall_score(y_test, test_predictions, zero_division=0))
print("Test F1:", f1_score(y_test, test_predictions, zero_division=0))

print("\nTest Confusion Matrix:")
print(confusion_matrix(y_test, test_predictions))