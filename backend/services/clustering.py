import pandas as pd
import numpy as np


def prepare_features(df):

    df = df.copy()

    # Remove columns not used for clustering
    df = df.drop(columns=[
        "CustomerID",
        "BasketValue",
        "TotalOrders",
        "CancelledOrders",
        "DaysSinceLastPurchase"
    ])

    # Log-transform skewed features
    skewed = [
        "Monetary",
        "Frequency",
        "AverageOrderValue",
        "TotalQuantity"
    ]

    for col in skewed:
        df[col] = np.log1p(df[col])

    return df

from sklearn.preprocessing import StandardScaler


def scale_features(df):

    scaler = StandardScaler()

    scaled = scaler.fit_transform(df)

    return scaled, scaler

from sklearn.cluster import KMeans


def elbow_method(data):

    inertia = []

    for k in range(2, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(data)

        inertia.append(model.inertia)

    return inertia

from sklearn.metrics import silhouette_score


def silhouette_scores(data):

    scores = []

    for k in range(2, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(data)

        score = silhouette_score(data, labels)

        scores.append(score)

    return scores

def train_kmeans(data, k):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(data)

    return model, labels

def assign_segments(customer_df, labels):

    result = customer_df.copy()

    result["Cluster"] = labels

    return result