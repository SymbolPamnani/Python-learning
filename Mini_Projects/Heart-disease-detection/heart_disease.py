import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("DecodeLabs_internship/Project2/heart.csv")

# EDA

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:")
df.info()

print("\nDescriptive Statistics:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nTarget Distribution:")
print(df["target"].value_counts())

#Target distribution
plt.figure(figsize=(6, 4))

sns.countplot(data=df, x="target")

plt.title("Target Class Distribution")
plt.xlabel("Target")
plt.ylabel("Count")
plt.show()

#Feature Distribution
numeric_columns = [
    "age",
    "resting_bp",
    "cholestoral",
    "max_hr",
    "oldpeak"
]

for column in numeric_columns:

    plt.figure(figsize=(6, 4))

    sns.histplot(data=df, x=column, kde=True)

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.show()


#Categorical
categorical_columns = [
    "sex",
    "chest_pain_type",
    "fasting_blood_sugar",
    "restecg",
    "exang",
    "slope",
    "num_major_vessels",
    "thal"
]

for column in categorical_columns:

    plt.figure(figsize=(6, 4))

    sns.countplot(data=df, x=column)

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Count")

    plt.show()

#Correlation
plt.figure(figsize=(12, 8))

sns.heatmap(
    df.corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Feature Correlation Heatmap")
plt.show()

#Data cleaning
# Check for missing values
missing_values = df.isnull().sum()
if missing_values.sum() == 0:
    print("\nNo missing values found.")

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
if duplicate_rows == 0:
    print("No duplicate rows found.")

print("\nMissing values:")
print(missing_values)

print("\nDuplicate rows:", duplicate_rows)

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)
print("Training targets:", y_train.shape)
print("Testing targets:", y_test.shape)

logistic_model = LogisticRegression(max_iter=1000)

logistic_model.fit(X_train_scaled, y_train)

y_pred_logistic = logistic_model.predict(X_test_scaled)

print("Logistic Predictions:")
print(y_pred_logistic)

knn_model = KNeighborsClassifier(n_neighbors=5)

knn_model.fit(X_train_scaled, y_train)

y_pred_knn = knn_model.predict(X_test_scaled)

print("KNN Predictions:")
print(y_pred_knn)

tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train, y_train)

y_pred_tree = tree_model.predict(X_test)

print("Decision Tree Predictions:")
print(y_pred_tree)

def evaluate_model(model_name, y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)

    print(f"\n{model_name}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)

    return accuracy, precision, recall, f1

logistic_results = evaluate_model("Logistic Regression", y_test, y_pred_logistic)

knn_results = evaluate_model("KNN", y_test, y_pred_knn)

tree_results = evaluate_model("Decision Tree", y_test, y_pred_tree)

results = pd.DataFrame(
    [logistic_results, knn_results, tree_results],
    columns=["Accuracy", "Precision", "Recall", "F1 Score"],
    index=["Logistic Regression", "KNN", "Decision Tree"]
)

print("\nModel Comparison:")
print(results)

best_model = results["F1 Score"].idxmax()
best_score = results["F1 Score"].max()

print(f"\nBest model based on F1 Score: {best_model}")
print(f"F1 Score: {best_score:.4f}")

models = {
    "Logistic Regression": y_pred_logistic,
    "KNN": y_pred_knn,
    "Decision Tree": y_pred_tree
}

for name, predictions in models.items():

    cm = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["No Disease", "Disease"],
        yticklabels=["No Disease", "Disease"]
    )

    plt.title(f"{name} - Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

# =========================
# New Patient Prediction
# =========================

print("\n==============================")
print("NEW PATIENT PREDICTION")
print("==============================")

age = float(input("Enter age: "))
sex = float(input("Enter sex (0 = female, 1 = male): "))
chest_pain_type = float(input("Enter chest pain type (0-3): "))
resting_bp = float(input("Enter resting blood pressure: "))
cholestoral = float(input("Enter cholesterol: "))
fasting_blood_sugar = float(input("Enter fasting blood sugar (0 or 1): "))
restecg = float(input("Enter resting ECG result (0-2): "))
max_hr = float(input("Enter maximum heart rate: "))
exang = float(input("Enter exercise-induced angina (0 or 1): "))
oldpeak = float(input("Enter oldpeak: "))
slope = float(input("Enter slope (0-2): "))
num_major_vessels = float(input("Enter number of major vessels (0-3): "))
thal = float(input("Enter thal value: "))

new_patient = pd.DataFrame([[
    age,
    sex,
    chest_pain_type,
    resting_bp,
    cholestoral,
    fasting_blood_sugar,
    restecg,
    max_hr,
    exang,
    oldpeak,
    slope,
    num_major_vessels,
    thal
]], columns=X.columns)

new_patient_scaled = scaler.transform(new_patient)

prediction = logistic_model.predict(new_patient_scaled)

print("\nPrediction:")

if prediction[0] == 1:
    print("The model predicts: Disease")
else:
    print("The model predicts: No Disease")

probabilities = logistic_model.predict_proba(new_patient_scaled)

print(f"Probability of No Disease: {probabilities[0][0]:.2%}")
print(f"Probability of Disease: {probabilities[0][1]:.2%}")