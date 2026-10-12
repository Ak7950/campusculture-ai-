from fastapi import FastAPI

from .agent import generate_plan
from .schemas import PlanRequest, PlanResponse

app = FastAPI(
    title="CampusCulture AI",
    description="Audience-aware cultural event planning for college societies.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CampusCulture AI"}


@app.post("/api/plan", response_model=PlanResponse)
def create_plan(request: PlanRequest) -> PlanResponse:
    """Generate a plan using available candidates and curated fallbacks.

    Qloo candidates will be injected here once live API integration is ready.
    An empty candidate list must never be represented as live Qloo evidence.
    """
    return generate_plan(request, candidates=[])
