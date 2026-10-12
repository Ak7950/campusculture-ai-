"""Pydantic v2 contract for POST /api/plan."""
from enum import Enum
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)


class Category(str, Enum):
    theme = 'theme'
    music = 'music'
    activities = 'activities'
    food = 'food'


class AudienceProfile(ContractModel):
    name: str = Field(default='Primary audience', min_length=1)
    interests: list[str] = Field(min_length=1, max_length=20)
    location: str = Field(min_length=1)
    event_type: str = Field(min_length=1)

    @field_validator('interests')
    @classmethod
    def clean_interests(cls, values):
        result = list(dict.fromkeys(v.strip() for v in values if v.strip()))
        if not result:
            raise ValueError('Interests cannot be empty')
        return result


class PlanRequest(ContractModel):
    audience: AudienceProfile
    budget_per_person: float = Field(ge=.01, multiple_of=.01, allow_inf_nan=False)
    attendees: int = Field(ge=1, strict=True)
    currency: Literal['INR'] = 'INR'
    constraints: list[str] = Field(default_factory=list)
    rejected_ids: list[str] = Field(default_factory=list)


class CulturalCandidate(ContractModel):
    """Internal input supplied by the backend, never by the public request."""
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category: Category
    score: float = Field(default=.5, ge=0, le=1, allow_inf_nan=False)
    tags: list[str] = Field(default_factory=list)
    source: Literal['qloo', 'mock', 'curated'] = 'curated'
    source_id: str | None = Field(default=None, min_length=1)
    evidence: str | None = None

    @model_validator(mode='after')
    def require_qloo_identifier(self):
        if self.source == 'qloo' and not self.source_id:
            raise ValueError('Qloo candidates require an actual source_id')
        return self


class QlooEvidence(ContractModel):
    source_id: str
    signal: str | None = None


class Recommendation(ContractModel):
    id: str
    category: Category
    title: str
    reason: str
    source: Literal['qloo', 'mock', 'curated']
    qloo_evidence: QlooEvidence | None = None
    rank_score: float = Field(ge=0, le=1, allow_inf_nan=False)


class BudgetItem(ContractModel):
    category: str
    amount: float = Field(ge=0, allow_inf_nan=False)
    share_percent: float = Field(ge=0, le=100, allow_inf_nan=False)


class BudgetEstimate(ContractModel):
    breakdown: list[BudgetItem]
    total: float = Field(gt=0, allow_inf_nan=False)
    budget_per_person: float = Field(gt=0, allow_inf_nan=False)
    attendees: int = Field(ge=1)
    currency: Literal['INR'] = 'INR'
    assumptions: list[str]


class EventPlan(ContractModel):
    title: str
    theme: str
    recommendations: list[Recommendation]
    budget_estimate: BudgetEstimate
    alternatives: list[Recommendation]
    warnings: list[str]
    evidence_status: Literal['qloo', 'mixed', 'mock', 'curated', 'none']
    audience_name: str


class PlanComparison(ContractModel):
    """Future transparent evaluation; criteria must identify their method."""
    criteria: list[str]
    observations: list[str]
    limitations: list[str]


class PlanResponse(EventPlan):
    baseline: EventPlan | None = None
    comparison: PlanComparison | None = None
