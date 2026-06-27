from fastapi import APIRouter
import pandas as pd
import os

from services.clustering import run_segmentation
from services.profiling import profile_clusters
from services.rfm import generate_rfm_segments
from services.value_analysis import generate_clv_segments

router = APIRouter()


@router.post("/segment")
def run_segmentation_api():

    input_file = "outputs/customer_analytics.csv"

    if not os.path.exists(input_file):
        return {
            "error": "Run analytics first."
        }

    customer_df = pd.read_csv(input_file)

    segments = run_segmentation(customer_df, k=4)

    output_file = "outputs/customer_segments.csv"

    segments.to_csv(output_file, index=False)

    profiles = profile_clusters(segments)

    profiles.to_csv(
        "outputs/cluster_profiles.csv",
        index=False
    )

    rfm = generate_rfm_segments(customer_df)

    rfm.to_csv(
        "outputs/rfm_segments.csv",
        index=False
    )

    clv = generate_clv_segments(customer_df)

    clv.to_csv(
        "outputs/clv_segments.csv",
        index=False
    )

    return {
        "message": "Segmentation completed.",
        "customers": len(segments),
        "clusters": segments["Cluster"].nunique(),
        "output": output_file
    }