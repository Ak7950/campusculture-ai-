import pytest
from pydantic import ValidationError
from app.schemas import PlanRequest, CulturalCandidate
from app.agent import generate_plan

def brief():
    return PlanRequest(audience={'name':'Indie fans','interests':['indie','music']},
                       event_type='concert',location='Patiala',attendees=100,
                       budget=50000, constraints=['No alcohol'])

def test_fallback_and_budget():
    p = generate_plan(brief()).plan
    assert p.theme and p.evidence_status == 'curated'
    assert round(sum(x.amount for x in p.budget),2) == 50000
    assert len(p.music) == 1

def test_rank_and_attribution():
    candidates = [
        CulturalCandidate(id='low',name='Rock',category='music',score=.1,source='mock'),
        CulturalCandidate(id='high',name='Indie music',category='music',score=.95,
                          source='qloo',source_id='entity-123',evidence='External test evidence'),
    ]
    p = generate_plan(brief(), candidates).plan
    assert p.music[0].id == 'high'
    assert p.music[0].evidence == 'External test evidence'
    assert p.evidence_status == 'mixed'

def test_rejections():
    p = brief()
    p.rejected_ids = ['curated-music']
    assert generate_plan(p).plan.music == []

def test_exclusions():
    candidates = [CulturalCandidate(id='beer',name='Beer tasting',category='food',score=1)]
    p = generate_plan(brief(), candidates).plan
    assert all(i.id != 'beer' for i in p.food)

def test_invalid_budget():
    data = brief().model_dump()
    data['budget'] = 0
    with pytest.raises(ValidationError): PlanRequest(**data)

def test_missing_interests():
    data = brief().model_dump()
    data['audience']['interests'] = [' ']
    with pytest.raises(ValidationError): PlanRequest(**data)
