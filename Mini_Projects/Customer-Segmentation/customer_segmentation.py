import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ------------------
# 2. LOAD DATASET
# ------------------

data = pd.read_csv("Python-learning/Mini_Projects/Customer-Segmentation/customer_segmentation.csv")

# ----------------------------
# 3. BASIC DATASET INSPECTION
# ----------------------------

print("First 5 rows:")
print(data.head())

print("\nDataset shape:")
print(data.shape)

print("\nColumn names:")
print(data.columns)

print("\nDataset information:")
data.info()

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate rows:")
print(data.duplicated().sum())

print("\nStatistical summary:")
print(data.describe())


# ------------------------------------
# 4. EXPLORATORY DATA ANALYSIS (EDA)
# ------------------------------------

# Distribution of numerical features

data.hist(figsize=(12, 8))
plt.suptitle("Customer Feature Distributions")
plt.tight_layout()
plt.show()

# Correlation between numerical features

plt.figure(figsize=(8, 6))
sns.heatmap(
    data.drop(columns=["CustomerID"]).corr(),
    annot=True, cmap="coolwarm")
plt.title("Feature Correlation")
plt.show()


# ------------------------------------
# 5. SELECT FEATURES FOR CLUSTERING
# ------------------------------------

features = data[
    [
        "Age",
        "AnnualIncome_kUSD",
        "SpendingScore",
        "PurchaseFrequency",
        "OnlinePurchaseRatio"
    ]
]

print("\nSelected features:")
print(features.head())

print("\nFeature shape:")
print(features.shape)


# ----------------------
# 6. FEATURE SCALING
# ----------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)
print("\nScaled feature sample:")
print(X_scaled[:5])


# --------------------------------------------------------------
# 7. FIND THE OPTIMAL NUMBER OF CLUSTERS USING THE ELBOW METHOD
# --------------------------------------------------------------

inertia_values = []
k_values = range(1, 11)

for k in k_values:

    model = KMeans( n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    inertia_values.append(model.inertia_)

# Plot the Elbow Curve

plt.figure(figsize=(8, 5))
plt.plot( k_values, inertia_values, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia / WCSS")
plt.title("Elbow Method")
plt.xticks(k_values)
plt.show()


# ------------------------------------
# 8. COMPARE SILHOUETTE SCORES
# ------------------------------------

silhouette_values = []

# Silhouette score cannot be calculated for K = 1, so we start from K = 2.

for k in range(2, 11):

    model = KMeans(n_clusters=k, random_state=42, n_init=10)

    labels = model.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_values.append(score)

    print(
        f"K = {k} | "
        f"Silhouette Score = {score:.4f}")

# Plot silhouette scores

plt.figure(figsize=(8, 5))
plt.plot(range(2, 11), silhouette_values, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Score Comparison")
plt.xticks(range(2, 11))
plt.show()

# ------------------------------------
# 9. CREATE FINAL K-MEANS MODEL
# ------------------------------------

optimal_k = range(2, 11)[np.argmax(silhouette_values)]
final_model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)

# ---------------------------------------
# 10. TRAIN K-MEANS AND ASSIGN CLUSTERS
# ---------------------------------------

cluster_labels = final_model.fit_predict(X_scaled)


# Add cluster labels to the original dataset

data["Cluster"] = cluster_labels

print("\nCluster assignments:")
print(data[["CustomerID", "Cluster"]].head(20))

# -----------------------
# 11. FINAL CENTROIDS
# -----------------------

print("\nCluster centroids:")
print(final_model.cluster_centers_)

# -----------------------------------------
# 12. NUMBER OF CUSTOMERS IN EACH CLUSTER
# -----------------------------------------

print("\nCustomers per cluster:")
print(data["Cluster"].value_counts().sort_index())

# ---------------------
# 13. CLUSTER PROFILE
# ---------------------

cluster_profile = data.groupby("Cluster")[
    [
        "Age",
        "AnnualIncome_kUSD",
        "SpendingScore",
        "PurchaseFrequency",
        "OnlinePurchaseRatio"
    ]
].mean()


print("\nCluster Profiles:")
print(cluster_profile)


# ---------------------------------
# 14. VISUALIZE CUSTOMER CLUSTERS
# ---------------------------------

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=data,
    x="AnnualIncome_kUSD",
    y="SpendingScore",
    hue="Cluster",
    palette="viridis",
    s=80
)

plt.title("Customer Segmentation")
plt.xlabel("Annual Income (kUSD)")
plt.ylabel("Spending Score")
plt.show()


# --------------------------------------
# 15. VISUALIZE CLUSTERS WITH CENTROIDS
# --------------------------------------

# We use the original income and spending features for an easier-to-understand visualization.

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=data,
    x="AnnualIncome_kUSD",
    y="SpendingScore",
    hue="Cluster",
    palette="viridis",
    s=80
)

# Convert scaled centroids back to original units

centroids_original = scaler.inverse_transform(final_model.cluster_centers_)

plt.scatter(
    centroids_original[:, 1],
    centroids_original[:, 2],
    marker="X",
    s=250,
    color="black",
    label="Centroids"
)

plt.title("Customer Clusters with Centroids")
plt.xlabel("Annual Income (kUSD)")
plt.ylabel("Spending Score")
plt.legend()
plt.show()


# ---------------------------------------
# 16. PREDICT CLUSTER FOR A NEW CUSTOMER
# ---------------------------------------

new_customer = pd.DataFrame({
    "Age": [30],
    "AnnualIncome_kUSD": [70],
    "SpendingScore": [80],
    "PurchaseFrequency": [9],
    "OnlinePurchaseRatio": [0.75]
})

new_customer_scaled = scaler.transform(new_customer)

new_customer_cluster = final_model.predict(new_customer_scaled)

print(
    "New customer belongs to Cluster:",
    new_customer_cluster[0]
)