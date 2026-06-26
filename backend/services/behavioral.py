import pandas as pd


def generate_behavior_features(df):

    purchases = df[
        (~df["InvoiceNo"].astype(str).str.startswith("C"))
        & (df["Quantity"] > 0)
    ].copy()

    purchases["Revenue"] = (
        purchases["Quantity"] *
        purchases["UnitPrice"]
    )

    behavior = (
        purchases.groupby("CustomerID")
        .agg(
            ProductDiversity=("StockCode", "nunique"),

            BasketValue=("Revenue", "mean"),

            TotalQuantity=("Quantity", "sum")
        )
        .reset_index()
    )

    return behavior