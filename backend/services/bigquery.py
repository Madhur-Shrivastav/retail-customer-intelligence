import os
import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account

from config import PROJECT_ID, DATASET_ID, KEY_PATH


credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

print("CLIENT PROJECT:", client.project)

def upload_csv(csv_path, table_name):

    if not os.path.exists(csv_path):
        return {
            "table": table_name,
            "status": "File not found"
        }

    df = pd.read_csv(csv_path)

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE"
        )
    )

    job.result()

    return {
        "table": table_name,
        "rows": len(df),
        "status": "Uploaded"
    }


def ingest_outputs_to_bigquery():

    results = []

    files = {

        "customer_analytics":
            "outputs/customer_analytics.csv",

        "rfm_segments":
            "outputs/rfm_segments.csv",

        "rfm_cluster_profiles":
            "outputs/rfm_cluster_profiles.csv",

        "clv_segments":
            "outputs/clv_segments.csv",

        "clv_cluster_profiles":
            "outputs/clv_cluster_profiles.csv",

        "customer_segments":
            "outputs/customer_segments.csv",

        "cluster_profiles":
            "outputs/cluster_profiles.csv"

    }

    for table, file in files.items():

        results.append(
            upload_csv(file, table)
        )

    return {
        "status": "success",
        "tables": results
    }