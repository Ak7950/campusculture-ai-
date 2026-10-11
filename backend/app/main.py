
from fastapi import FastAPI

app = FastAPI(
    title="CampusCulture AI",
    description="Audience-aware cultural event planning for college societies.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CampusCulture AI"}
