import pandas as pd
import joblib
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.txt"


# Load trained model
model = joblib.load(MODEL_PATH)

# Load optimized threshold
with open(THRESHOLD_PATH, "r") as file:
    threshold = float(file.read())

print("Model loaded successfully.")
print("Threshold:", threshold)

# Example customer
customer = pd.DataFrame([{
    "Age": 45,
    "Tenure_Months": 12,
    "Monthly_Charges": 120.50,
    "Total_Charges": 1446.00,
    "Support_Calls": 4,
    "Payment_Delays": 3,
    "Num_Products": 2,
    "Contract_Length": "Monthly",
    "Has_Internet": "Yes",
    "Has_Streaming": "Yes",
    "Gender": "Male"
}])


# Get churn probability
churn_probability = model.predict_proba(customer)[0][1]

# Apply optimized threshold
prediction = int(churn_probability >= threshold)

print("\nCustomer Prediction")
print("----------------------")

print("Churn Probability:",round(churn_probability, 3))
print("Threshold:",threshold)
print("Prediction:",prediction)

if prediction == 1:
    print("Result: Customer is likely to churn.")
else:
    print("Result: Customer is likely to stay.")