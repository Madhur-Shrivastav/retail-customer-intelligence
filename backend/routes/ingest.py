from fastapi import APIRouter

from services.bigquery import ingest_outputs_to_bigquery

router = APIRouter()


@router.post("/ingest")
def ingest():

    return ingest_outputs_to_bigquery()