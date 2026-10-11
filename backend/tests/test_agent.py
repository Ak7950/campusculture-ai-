import json
from decimal import Decimal
from pathlib import Path
import pytest
from pydantic import ValidationError
from app.schemas import PlanRequest, PlanResponse, CulturalCandidate
from app.agent import generate_plan, allocation


def brief():
    return PlanRequest(audience={'interests': ['indie music', 'anime'],
                                'location': 'Chandigarh', 'event_type': 'campus social'},
                       budget_per_person=500, attendees=100, constraints=['campus venue'])


def candidate(id, **kwargs):
    return CulturalCandidate(id=id, name=kwargs.pop('name', 'Indie music'),
                             category='music', **kwargs)


def test_agreed_contract_and_round_trip():
    response = generate_plan(brief())
    payload = response.model_dump(mode='json')
    assert {'title', 'theme', 'recommendations', 'budget_estimate', 'alternatives',
            'baseline', 'comparison'} <= payload.keys()
    assert 'plan' not in payload
    assert payload['budget_estimate']['total'] == 50000
    assert payload['baseline'] is None and payload['comparison'] is None
    assert PlanResponse.model_validate_json(response.model_dump_json()) == response
    assert response.budget_estimate.assumptions
    assert response.evidence_status == 'curated'
    assert all(r.qloo_evidence is None for r in response.recommendations)


def test_rank_and_evidence_passthrough():
    response = generate_plan(brief(), [
        candidate('low', score=.1, source='mock', evidence='Ignore this'),
        candidate('high', score=.95, source='qloo', source_id='fixture-entity',
                  evidence='Synthetic test fixture, not a real API result'),
    ])
    music = [r for r in response.recommendations if r.category == 'music']
    assert music[0].id == 'high'
    assert music[0].qloo_evidence.source_id == 'fixture-entity'
    assert music[0].qloo_evidence.signal == 'Synthetic test fixture, not a real API result'
    assert music[1].qloo_evidence is None
    assert response.evidence_status == 'mixed'


def test_alternatives_and_rejection():
    rows = [candidate(str(i), score=1-i*.1) for i in range(4)]
    response = generate_plan(brief(), rows)
    assert [r.id for r in response.alternatives] == ['2', '3']
    request = brief().model_copy(update={'rejected_ids': ['0', 'curated-food']})
    revised = generate_plan(request, rows)
    assert all(r.id not in request.rejected_ids for r in revised.recommendations + revised.alternatives)
    assert [r.id for r in revised.recommendations if r.category == 'music'] == ['1', '2']


def test_constraint_filters_alternatives_too():
    request = brief().model_copy(update={'constraints': ['No alcohol']})
    rows = [candidate('beer', name='Beer tasting', score=1)]
    response = generate_plan(request, rows)
    assert all(r.id != 'beer' for r in response.recommendations + response.alternatives)


@pytest.mark.parametrize('value', [0, -1, float('nan'), float('inf'), .001, 1.001])
def test_invalid_budget(value):
    data = brief().model_dump()
    data['budget_per_person'] = value
    with pytest.raises(ValidationError):
        PlanRequest.model_validate(data)


@pytest.mark.parametrize('value', [0, -1, 1.5, True, '100'])
def test_invalid_attendees(value):
    data = brief().model_dump()
    data['attendees'] = value
    with pytest.raises(ValidationError):
        PlanRequest.model_validate(data)


def test_old_contract_rejected():
    data = brief().model_dump()
    data['budget'] = 50000
    with pytest.raises(ValidationError):
        PlanRequest.model_validate(data)


@pytest.mark.parametrize('field,value', [('interests', [' ']), ('location', ' '), ('event_type', ' ')])
def test_empty_audience_fields(field, value):
    data = brief().model_dump()
    data['audience'][field] = value
    with pytest.raises(ValidationError):
        PlanRequest.model_validate(data)


def test_unattributed_qloo_rejected():
    with pytest.raises(ValidationError):
        candidate('qloo', source='qloo')


@pytest.mark.parametrize('total', ['0.01', '0.02', '0.03', '1.01', '50000.00'])
def test_budget_conservation(total):
    items = allocation(Decimal(total))
    assert sum(Decimal(str(x.amount)) for x in items) == Decimal(total)
    assert all(x.amount >= 0 for x in items)


def test_sample_profiles():
    rows = json.loads(Path(__file__).with_name('sample_profiles.json').read_text())
    assert len(rows) == 3
    for row in rows:
        assert generate_plan(PlanRequest.model_validate(row)).title
