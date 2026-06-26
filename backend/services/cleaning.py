import pandas as pd

def clean_data(filepath):

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Standardize column names
    df.columns = df.columns.str.strip()

    df.rename(columns={
        "Invoice": "InvoiceNo",
        "Customer ID": "CustomerID",
        "Price": "UnitPrice"
    }, inplace=True)

    # Remove rows without CustomerID
    df = df.dropna(subset=["CustomerID"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert InvoiceDate
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Create Revenue
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    return df