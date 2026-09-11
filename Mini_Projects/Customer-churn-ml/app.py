import pandas as pd
import joblib
import streamlit as st
from pathlib import Path


# Project Paths
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.txt"

# Page Configuration
st.set_page_config(page_title="Customer Churn Predictor", layout="wide")

# Load Model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_resource
def load_threshold():
    with open(THRESHOLD_PATH, "r") as file:
        return float(file.read())

model = load_model()
threshold = load_threshold()

# Page Header
st.title("📊 Customer Churn Prediction")

st.write(
    "Predict whether a customer is likely to churn based on "
    "their demographic, usage, billing, and service information."
)

st.info(f"Current decision threshold: **{threshold:.2f}**")

# Customer Information
st.subheader("Customer Information")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=40)
    tenure = st.number_input("Tenure (Months)", min_value=1, max_value=120, value=12)
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=80.0, step=0.01)
    total_charges = st.number_input("Total Charges", min_value=0.0, value=1000.0, step=0.01)
    support_calls = st.number_input("Support Calls", min_value=0, max_value=50, value=2)
    payment_delays = st.number_input("Payment Delays", min_value=0, max_value=50, value=1)

with col2:
    num_products = st.number_input("Number of Products", min_value=1, max_value=20, value=2)
    contract_length = st.selectbox("Contract Length", ["Monthly", "Yearly", "Two Year"])
    has_internet = st.selectbox("Has Internet", ["Yes", "No"])
    has_streaming = st.selectbox("Has Streaming", ["Yes", "No"])
    gender = st.selectbox("Gender", ["Male", "Female"])

# Prediction
if st.button("Predict Churn", use_container_width=True):

    customer = pd.DataFrame([{
        "Age": age,
        "Tenure_Months": tenure,
        "Monthly_Charges": monthly_charges,
        "Total_Charges": total_charges,
        "Support_Calls": support_calls,
        "Payment_Delays": payment_delays,
        "Num_Products": num_products,
        "Contract_Length": contract_length,
        "Has_Internet": has_internet,
        "Has_Streaming": has_streaming,
        "Gender": gender
    }])

    # Get churn probability
    churn_probability = model.predict_proba(customer)[0][1]

    # Apply optimized threshold
    prediction = int(churn_probability >= threshold)
    probability_percentage = (churn_probability * 100)

    # Display Results
    st.divider()
    st.subheader("Prediction Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Churn Probability", f"{probability_percentage:.1f}%")
    with col2:
        st.metric("Decision Threshold", f"{threshold * 100:.0f}%")
    with col3:
        if prediction == 1:
            st.metric("Prediction", "Likely to Churn")
        else:
            st.metric("Prediction", "Likely to Stay")


    # Risk Message
    if prediction == 1:
        st.error(
            "**High Churn Risk** — "
            "The model predicts that this customer is likely to churn.")
    else:
        st.success(
            "**Lower Churn Risk** — "
            "The model predicts that this customer is likely to stay.")

    # Probability bar
    st.write("### Churn Probability")
    st.progress(min(churn_probability, 1.0))
    st.caption(
        "The probability represents the model's estimated likelihood "
        "that the customer belongs to the churn class.")


# Model Information
with st.expander("ℹ️ About this model"):

    st.write(
        "This application uses a Logistic Regression classification "
        "model with preprocessing for numerical and categorical features.")

    st.write(
        "The model uses class balancing because churned customers "
        "represent a minority of the dataset.")

    st.write(
        f"The classification threshold was optimized using "
        f"5-fold cross-validation and selected as **{threshold:.2f}** "
        f"based on F1 score.")