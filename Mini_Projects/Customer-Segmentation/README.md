# Customer Segmentation using K-Means Clustering

## Overview

This mini project implements an unsupervised machine learning pipeline to segment customers into groups based on their characteristics and purchasing behavior.

The project uses **K-Means Clustering** to identify customer groups without predefined labels. The clustering process is evaluated using the **Elbow Method** and **Silhouette Score** to determine a suitable number of clusters.

## Dataset

The dataset contains **510 customer records** with the following features:

* `CustomerID` — Unique customer identifier
* `Age` — Customer age
* `AnnualIncome_kUSD` — Annual income in thousands of USD
* `SpendingScore` — Customer spending score
* `PurchaseFrequency` — Average purchase frequency
* `OnlinePurchaseRatio` — Proportion of purchases made online

There are no missing values or duplicate records in the dataset.

## Project Workflow

```text
Dataset
   ↓
Data Inspection
   ↓
Exploratory Data Analysis
   ↓
Feature Selection
   ↓
Feature Scaling
   ↓
Elbow Method
   ↓
Silhouette Score
   ↓
K-Means Clustering
   ↓
Cluster Analysis
   ↓
Visualization
   ↓
New Customer Prediction
```

## Methodology

### 1. Data Inspection

The dataset is inspected for:

* Shape and structure
* Data types
* Missing values
* Duplicate records
* Statistical information

### 2. Exploratory Data Analysis

Histograms and a correlation heatmap are used to understand feature distributions and relationships.

### 3. Feature Selection

`CustomerID` is excluded because it is an identifier rather than a meaningful customer characteristic.

The following features are used for clustering:

```text
Age
AnnualIncome_kUSD
SpendingScore
PurchaseFrequency
OnlinePurchaseRatio
```

### 4. Feature Scaling

`StandardScaler` is used to standardize the features.

This is important because K-Means relies on distance calculations, and features with larger numerical ranges could otherwise dominate the clustering process.

### 5. Choosing the Number of Clusters

Two approaches are used:

* **Elbow Method** — evaluates cluster compactness using inertia/WCSS.
* **Silhouette Score** — evaluates how well-separated the resulting clusters are.

For this dataset, the highest silhouette score was obtained with:

```text
K = 2
Silhouette Score = 0.3709
```

Therefore, two clusters were selected for the final model.

## Results

The final K-Means model produced two customer segments.

### Cluster 0 — High-Engagement Customers

Average characteristics:

* Spending Score: **73.70**
* Purchase Frequency: **8.08**
* Online Purchase Ratio: **0.75**

These customers demonstrate relatively high purchasing activity and spending.

### Cluster 1 — Low-Engagement Customers

Average characteristics:

* Spending Score: **28.22**
* Purchase Frequency: **3.12**
* Online Purchase Ratio: **0.44**

These customers demonstrate relatively lower purchasing activity and spending.

The model can also assign a new customer's data to one of the discovered clusters.

## Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Scikit-learn

## Key Concepts Practiced

* Unsupervised Learning
* K-Means Clustering
* Euclidean Distance
* Centroids
* Feature Scaling
* Elbow Method
* Inertia / WCSS
* Silhouette Score
* Cluster Profiling
* Data Visualization
* New Data Prediction

## Files

```text
Customer-Segmentation/
│
├── customer_segmentation.py
├── customer_segmentation.csv
└── README.md
```

## How to Run

Clone the repository and run:

```bash
python customer_segmentation.py
```

Make sure the required libraries are installed:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Conclusion

This project demonstrates a complete K-Means clustering workflow, from raw customer data and exploratory analysis to feature scaling, cluster selection, segmentation, visualization, and prediction for new customers.

The project focuses on understanding **how and why K-Means works**, rather than simply using the algorithm as a pre-built function.