from services.rfm import generate_rfm
from services.value_analysis import generate_value_features


def generate_customer_features(df):

    rfm = generate_rfm(df)

    value = generate_value_features(df)

    customer = rfm.merge(value, on="CustomerID")

    return customer