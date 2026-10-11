"""CampusCulture v1 integration contract (Pydantic v2)."""
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator

class Category(str, Enum):
    theme = 'theme'
    music = 'music'
    activities = 'activities'
    food = 'food'

class AudienceProfile(BaseModel):
    name: str = Field(default='Primary audience', min_length=1)
    interests: list[str] = Field(min_length=1, max_length=20)
    @field_validator('interests')
    @classmethod
    def clean_interests(cls, v):
        result = list(dict.fromkeys(x.strip() for x in v if x.strip()))
        if not result: raise ValueError('Interests cannot be empty')
        return result

class PlanRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    audience: AudienceProfile
    event_type: str = Field(min_length=1)
    location: str = Field(min_length=1)
    attendees: int = Field(ge=1)
    budget: float = Field(gt=0, allow_inf_nan=False)
    currency: str = 'INR'
    constraints: list[str] = Field(default_factory=list)
    rejected_ids: list[str] = Field(default_factory=list)
    @field_validator('event_type', 'location')
    @classmethod
    def nonblank(cls, v):
        if not v.strip(): raise ValueError('Cannot be blank')
        return v.strip()

class CulturalCandidate(BaseModel):
    id: str
    name: str
    category: Category
    score: float = Field(default=.5, ge=0, le=1, allow_inf_nan=False)
    tags: list[str] = Field(default_factory=list)
    source: Literal['qloo', 'mock', 'curated'] = 'curated'
    source_id: str | None = None
    evidence: str | None = None

class Recommendation(BaseModel):
    id: str
    name: str
    category: Category
    reason: str
    source: Literal['qloo', 'mock', 'curated']
    source_id: str | None = None
    evidence: str | None = None
    rank_score: float

class BudgetItem(BaseModel):
    category: str
    amount: float = Field(ge=0)
    share_percent: float = Field(ge=0, le=100)

class EventPlan(BaseModel):
    theme: str
    music: list[Recommendation]
    activities: list[Recommendation]
    food: list[Recommendation]
    budget: list[BudgetItem]
    total_budget: float
    per_attendee: float
    currency: str
    warnings: list[str]
    evidence_status: Literal['qloo','mixed','mock','curated','none']
    audience_name: str

class PlanResponse(BaseModel):
    plan: EventPlan
    baseline: EventPlan | None = None
    comparison: dict | None = None
