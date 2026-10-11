
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="CampusCulture AI",
    description="Audience-aware cultural event planning for college societies.",
    version="0.1.0",
)


class AudienceProfile(BaseModel):
    interests: list[str] = Field(min_length=1)
    location: str = Field(min_length=1)
    event_type: str = Field(min_length=1)


class PlanRequest(BaseModel):
    audience: AudienceProfile
    budget_per_person: float = Field(gt=0)
    attendees: int = Field(gt=0)
    constraints: list[str] = Field(default_factory=list)


class BudgetSummary(BaseModel):
    total: float
    assumptions: list[str]


class PlanResponse(BaseModel):
    event_title: str
    theme: str
    recommendations: list[dict[str, Any]]
    budget: BudgetSummary
    alternatives: list[dict[str, Any]]
    qloo_used: bool
    mode: str


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CampusCulture AI"}


@app.post("/api/plan", response_model=PlanResponse)
def create_plan(request: PlanRequest):
    """Temporary contract stub; real Qloo and agent integration comes later."""
    budget_ceiling = request.budget_per_person * request.attendees

    return PlanResponse(
        event_title="Development placeholder — no plan generated yet",
        theme="Mock response for integration testing",
        recommendations=[],
        budget=BudgetSummary(
            total=budget_ceiling,
            assumptions=[
                "Budget ceiling calculated as budget_per_person × attendees.",
                "This is not a verified cost estimate.",
            ],
        ),
        alternatives=[],
        qloo_used=False,
        mode="mock",
    )
