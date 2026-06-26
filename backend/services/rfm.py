import pandas as pd


def generate_rfm(df):

    # Only completed purchases
    purchases = df[
        (~df["InvoiceNo"].astype(str).str.startswith("C"))
        & (df["Quantity"] > 0)
    ].copy()

    purchases["Revenue"] = (
        purchases["Quantity"] *
        purchases["UnitPrice"]
    )

    analysis_date = purchases["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = (
        purchases.groupby("CustomerID")
        .agg(
            Recency=("InvoiceDate",
                      lambda x: (analysis_date - x.max()).days),

            Frequency=("InvoiceNo", "nunique"),

            Monetary=("Revenue", "sum")
        )
        .reset_index()
    )

    return rfm