from services.rfm import generate_rfm
from services.value_analysis import generate_value_features
from services.behavioral import generate_behavior_features
from services.retention import generate_retention_features


def generate_customer_features(df):

    rfm = generate_rfm(df)

    value = generate_value_features(df)

    behavior = generate_behavior_features(df)

    retention = generate_retention_features(df)

    customer = rfm.merge(value, on="CustomerID")

    customer = customer.merge(behavior, on="CustomerID")

    customer = customer.merge(retention, on="CustomerID")

    return customer