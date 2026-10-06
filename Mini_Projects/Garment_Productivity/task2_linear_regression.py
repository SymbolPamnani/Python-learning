import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Set aesthetic style for Seaborn plots
sns.set_theme(style="whitegrid")


def setup_directories():
    """Create necessary directories for results and plots."""
    os.makedirs("results/plots", exist_ok=True)


def load_and_preprocess_data(filepath):
    """Load dataset, clean string values, and split features/target."""
    df = pd.read_csv(filepath)

    # Clean categorical string columns
    if "department" in df.columns:
        df["department"] = df["department"].str.strip().str.lower()

    # Drop date column or process temporal features if necessary
    if "date" in df.columns:
        df = df.drop(columns=["date"])

    target_col = "actual_productivity"
    X = df.drop(columns=[target_col])
    y = df[target_col]

    return df, X, y


def generate_eda_plots(df):
    """Generate and save Exploratory Data Analysis (EDA) visualizations."""
    print("Generating EDA plots...")

    # 1. Target Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["actual_productivity"], kde=True, color="skyblue")
    plt.title("Distribution of Actual Productivity")
    plt.xlabel("Actual Productivity")
    plt.savefig("results/plots/target_distribution.png", bbox_inches="tight")
    plt.close()

    # 2. Missing Values Visualization
    plt.figure(figsize=(8, 4))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Values Map")
    plt.savefig("results/plots/missing_values.png", bbox_inches="tight")
    plt.close()

    # 3. Correlation Heatmap for Numerical Columns
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Numerical Feature Correlation Heatmap")
    plt.savefig("results/plots/correlation_heatmap.png", bbox_inches="tight")
    plt.close()

    # 4. Productivity by Department
    if "department" in df.columns:
        plt.figure(figsize=(8, 5))
        sns.boxplot(
            data=df, x="department", y="actual_productivity", palette="Set2"
        )
        plt.title("Actual Productivity by Department")
        plt.savefig(
            "results/plots/productivity_by_department.png", bbox_inches="tight"
        )
        plt.close()


def build_preprocessor(X):
    """Construct column transformer pipeline for numerical and categorical features."""
    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()
    categorical_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    num_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler()),
        ]
    )

    cat_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_features),
            ("cat", cat_pipeline, categorical_features),
        ]
    )

    return preprocessor, numerical_features, categorical_features


def evaluate_model(model, X_test, y_test):
    """Compute performance metrics for a fitted model."""
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    return r2, rmse, mae, preds


def generate_residual_plots(y_test, predictions):
    """Plot residual distributions and actual vs predicted values."""
    residuals = y_test - predictions

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Actual vs Predicted
    sns.scatterplot(
        x=y_test, y=predictions, ax=axes[0], alpha=0.7, color="teal"
    )
    axes[0].plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        "r--",
        lw=2,
    )
    axes[0].set_title("Actual vs. Predicted Productivity")
    axes[0].set_xlabel("Actual")
    axes[0].set_ylabel("Predicted")

    # Residual Distribution
    sns.histplot(residuals, kde=True, ax=axes[1], color="purple")
    axes[1].set_title("Residuals Distribution")
    axes[1].set_xlabel("Residual (Actual - Predicted)")

    plt.tight_layout()
    plt.savefig("results/plots/residual_analysis.png", bbox_inches="tight")
    plt.close()


def save_feature_coefficients(ridge_model, preprocessor, X_train):
    """Extract and export Ridge regression feature coefficients."""
    # Extract feature names after encoding
    cat_encoder = (
        preprocessor.named_transformers_["cat"]
        .named_steps["encoder"]
    )
    cat_features = preprocessor.transformers_[1][2]
    
    if len(cat_features) > 0:
        encoded_cat_names = cat_encoder.get_feature_names_out(cat_features).tolist()
    else:
        encoded_cat_names = []

    num_features = preprocessor.transformers_[0][2]
    all_feature_names = num_features + encoded_cat_names

    coefs = ridge_model.named_steps["regressor"].coef_

    coef_df = pd.DataFrame({
        "feature": all_feature_names,
        "coefficient": coefs
    }).sort_values(by="coefficient", key=abs, ascending=False)

    coef_df.to_csv("results/feature_coefficients.csv", index=False)
    print("Feature coefficients saved to results/feature_coefficients.csv")


def main():
    setup_directories()

    data_path = "data/garments_worker_productivity.csv"
    if not os.path.exists(data_path):
        print(f"Error: Dataset file '{data_path}' not found.")
        return

    df, X, y = load_and_preprocess_data(data_path)
    print(f"Dataset shape: {df.shape}")

    # Generate Exploratory Visualizations
    generate_eda_plots(df)

    # Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_state=42, test_size=0.2
    ) if "test_state" in train_test_split.__code__.co_varnames else train_test_split(
        X, y, random_state=42, test_size=0.2
    )

    preprocessor, num_cols, cat_cols = build_preprocessor(X)

    # 1. Baseline Model (Mean Predictor)
    dummy_pipe = Pipeline(
        steps=[("preprocessor", preprocessor), ("regressor", DummyRegressor(strategy="mean"))]
    )
    dummy_pipe.fit(X_train, y_train)
    d_r2, d_rmse, d_mae, _ = evaluate_model(dummy_pipe, X_test, y_test)

    # 2. Linear Regression (OLS)
    lr_pipe = Pipeline(
        steps=[("preprocessor", preprocessor), ("regressor", LinearRegression())]
    )
    lr_pipe.fit(X_train, y_train)
    lr_r2, lr_rmse, lr_mae, _ = evaluate_model(lr_pipe, X_test, y_test)

    # 3. Ridge Regression with Hyperparameter CV Tuning
    alphas = np.logspace(-3, 3, 50)
    ridge_cv = RidgeCV(alphas=alphas, cv=5)
    ridge_pipe = Pipeline(
        steps=[("preprocessor", preprocessor), ("regressor", ridge_cv)]
    )
    ridge_pipe.fit(X_train, y_train)

    best_alpha = ridge_pipe.named_steps["regressor"].alpha_
    r_r2, r_rmse, r_mae, ridge_preds = evaluate_model(ridge_pipe, X_test, y_test)

    # 5-Fold Cross Validation Score for Best Ridge Model
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2_scores = cross_val_score(ridge_pipe, X, y, cv=kf, scoring="r2")

    # Display Metrics
    print("\n--- Model Comparison on Test Set ---")
    metrics_summary = pd.DataFrame(
        {
            "Model": ["Mean Baseline", "Linear Regression", f"Ridge (alpha={best_alpha:.3f})"],
            "R2 Score": [d_r2, lr_r2, r_r2],
            "RMSE": [d_rmse, lr_rmse, r_rmse],
            "MAE": [d_mae, lr_mae, r_mae],
        }
    )
    print(metrics_summary.to_string(index=False))

    print(f"\nRidge 5-Fold CV Mean R2: {cv_r2_scores.mean():.4f} (+/- {cv_r2_scores.std():.4f})")

    # Save outputs
    metrics_summary.to_csv("results/model_comparison.csv", index=False)
    
    predictions_df = pd.DataFrame({"actual": y_test, "predicted": ridge_preds})
    predictions_df.to_csv("results/predictions.csv", index=False)

    generate_residual_plots(y_test, ridge_preds)
    save_feature_coefficients(ridge_pipe, preprocessor, X_train)

    print("\nExecution complete. Outputs saved in 'results/' and 'results/plots/'.")


if __name__ == "__main__":
    main()