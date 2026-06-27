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

import pandas as pd


def assign_rfm_segment(row):

    r = row["R"]
    f = row["F"]
    m = row["M"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 4 and f >= 3:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "Potential Loyalists"

    elif r == 3 and f >= 3:
        return "Promising"

    elif r <= 2 and f >= 4:
        return "At Risk"

    elif r <= 2 and f <= 2 and m >= 3:
        return "Needs Attention"

    elif r <= 2 and f <= 2:
        return "Lost Customers"

    elif m >= 4:
        return "Big Spenders"

    else:
        return "Regular Customers"


def generate_rfm_segments(customer_df):

    df = customer_df.copy()

    # Lower Recency is better
    df["R"] = pd.qcut(
        df["Recency"],
        5,
        labels=[5, 4, 3, 2, 1]
    )

    # Higher Frequency is better
    df["F"] = pd.qcut(
        df["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )

    # Higher Monetary is better
    df["M"] = pd.qcut(
        df["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )

    df["R"] = df["R"].astype(int)
    df["F"] = df["F"].astype(int)
    df["M"] = df["M"].astype(int)

    df["RFMScore"] = (
        df["R"].astype(str)
        + df["F"].astype(str)
        + df["M"].astype(str)
    )

    df["RFMSegment"] = df.apply(
        assign_rfm_segment,
        axis=1
    )

    return df[
        [
            "CustomerID",
            "R",
            "F",
            "M",
            "RFMScore",
            "RFMSegment"
        ]
    ]