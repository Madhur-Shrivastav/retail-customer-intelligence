import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import matplotlib.pyplot as plt

def prepare_ml_data(customer_df):

    features = customer_df[
        [
            "Recency",
            "Frequency",
            "Monetary",
            "AverageOrderValue",
            "CustomerTenure",
            "ProductDiversity",
            "TotalQuantity",
            "ReturnRate"
        ]
    ].copy()

    # Log transform skewed features
    skewed = [
        "Monetary",
        "Frequency",
        "AverageOrderValue",
        "TotalQuantity"
    ]

    for col in skewed:
        features[col] = np.log1p(features[col])

    scaler = StandardScaler()

    scaled = scaler.fit_transform(features)

    feature_names = features.columns.tolist()

    return scaled, scaler, feature_names

def elbow_method(data):

    inertia = []

    for k in range(2,11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(data)

        inertia.append(model.inertia_)

    plt.figure(figsize=(6,4))

    plt.plot(range(2,11), inertia, marker="o")

    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")

    plt.savefig("outputs/ml/elbow_curve.png")

    plt.close()

    return inertia

def silhouette_analysis(data):

    scores = []

    for k in range(2,11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(data)

        score = silhouette_score(data, labels)

        scores.append(score)

    plt.figure(figsize=(6,4))

    plt.plot(range(2,11), scores, marker="o")

    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Analysis")

    plt.savefig("outputs/ml/silhouette.png")

    plt.close()

    return scores

def train_kmeans(data, k):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(data)

    return model, labels

def assign_clusters(customer_df, labels):

    result = customer_df.copy()

    result["Cluster"] = labels

    return result

def run_segmentation(customer_df, k=4):

    scaled, scaler, feature_names = prepare_ml_data(customer_df)

    elbow_method(scaled)

    silhouette_analysis(scaled)

    model, labels = train_kmeans(scaled, k)

    result = assign_clusters(customer_df, labels)

    return result
