import pandas as pd


def generate_retention_features(df):

    invoices = df.copy()

    invoices["IsCancelled"] = invoices["InvoiceNo"].astype(str).str.startswith("C")

    analysis_date = invoices["InvoiceDate"].max() + pd.Timedelta(days=1)

    retention = (
        invoices.groupby("CustomerID")
        .agg(
            LastPurchase=("InvoiceDate", "max"),

            TotalOrders=("InvoiceNo", "nunique"),

            CancelledOrders=("IsCancelled", "sum")
        )
        .reset_index()
    )

    retention["DaysSinceLastPurchase"] = (
        analysis_date -
        retention["LastPurchase"]
    ).dt.days

    retention["ReturnRate"] = (
        retention["CancelledOrders"] /
        retention["TotalOrders"]
    )

    retention.drop(
        columns=["LastPurchase"],
        inplace=True
    )

    return retention