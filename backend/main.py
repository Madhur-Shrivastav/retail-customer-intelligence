from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.analytics import router as analytics_router
from routes.segmentation import router as segmentation_router


app = FastAPI(
    title="Retail Customer Intelligence API"
)

app.include_router(upload_router)
app.include_router(analytics_router)
app.include_router(segmentation_router)

@app.get("/")
def home():
    return {"message": "Retail Customer Intelligence Platform"}