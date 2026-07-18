import pandas as pd

def profile_clusters(df):

    profile = (
        df.groupby("Cluster")
        .agg(
            Customers=("CustomerID", "count"),
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("Monetary", "mean"),
            AvgOrderValue=("AverageOrderValue", "mean"),
            AvgTenure=("CustomerTenure", "mean")
        )
        .round(2)
        .reset_index()
    )

    return profile

def profile_rfm_clusters(df):

    rfm_profile = (
        df.groupby("RFMSegment")
        .agg(
            Customers=("CustomerID", "count"),
            AvgR=("R", "mean"),
            AvgF=("F", "mean"),
            AvgM=("M", "mean")
        )
        .round(2)
        .reset_index()
    )

    return rfm_profile

def profile_clv_clusters(df):

    clv_profile = (
        df.groupby("CLVSegment")
        .agg(
            Customers=("CustomerID", "count"),
            AvgCLVScore=("CLVScore", "mean")
        )
        .round(2)
        .reset_index()
    )

    return clv_profile
