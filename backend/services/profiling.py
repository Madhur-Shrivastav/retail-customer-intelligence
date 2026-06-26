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

            AvgTenure=("CustomerTenure", "mean"),

            AvgProductDiversity=("ProductDiversity", "mean"),

            AvgQuantity=("TotalQuantity", "mean"),

            AvgReturnRate=("ReturnRate", "mean")
        )
        .round(2)
        .reset_index()
    )

    return profile