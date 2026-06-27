import pandas as pd


def generate_value_features(df):

    purchases = df[
        (~df["InvoiceNo"].astype(str).str.startswith("C"))
        &
        (df["Quantity"] > 0)
    ].copy()

    purchases["Revenue"] = (
        purchases["Quantity"]
        *
        purchases["UnitPrice"]
    )

    # ----------------------------
    # Invoice totals
    # ----------------------------

    invoice_totals = (
        purchases
        .groupby(
            ["CustomerID", "InvoiceNo"]
        )
        .agg(
            InvoiceValue=("Revenue", "sum"),
            InvoiceDate=("InvoiceDate", "max")
        )
        .reset_index()
    )

    # ----------------------------
    # Customer level features
    # ----------------------------

    customer = (
        invoice_totals
        .groupby("CustomerID")
        .agg(
            AverageOrderValue=("InvoiceValue", "mean"),

            FirstPurchase=("InvoiceDate", "min"),

            LastPurchase=("InvoiceDate", "max")
        )
        .reset_index()
    )

    customer["CustomerTenure"] = (
        customer["LastPurchase"]
        -
        customer["FirstPurchase"]
    ).dt.days

    customer.drop(
        columns=[
            "FirstPurchase",
            "LastPurchase"
        ],
        inplace=True
    )

    return customer


def generate_clv_segments(customer_df):

    df = customer_df.copy()

    # Simple CLV Score
    df["CLVScore"] = (
        df["Monetary"]
        * df["Frequency"]
        * (df["CustomerTenure"] + 1)
    ) / 365

    df["CLVSegment"] = pd.qcut(
        df["CLVScore"],
        5,
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Premium"
        ]
    )

    return df[
        [
            "CustomerID",
            "CLVScore",
            "CLVSegment"
        ]
    ]