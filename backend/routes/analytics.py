from fastapi import APIRouter

from services.cleaning import clean_data
from services.feature_engineering import generate_customer_features
from services.eda import run_eda

router = APIRouter()


@router.post("/analyse")
def run_analysis():

    input_file = "uploads/online_retail_II.xlsx"

    df = clean_data(input_file)

    customer_df = generate_customer_features(df)
    
    run_eda(customer_df)

    output_file = "outputs/customer_analytics.csv"

    customer_df.to_csv(output_file, index=False)

    return {
        "message": "Analysis completed successfully.",
        "customers": len(customer_df),
        "output": output_file
    }