"""Day 1 deterministic agent; Qloo candidates are injected by Avik's integration."""
import re
from .schemas import (Category, CulturalCandidate, Recommendation,
                      BudgetItem, EventPlan, PlanRequest, PlanResponse)

WEIGHTS = {'venue': 30, 'food': 25, 'production': 20, 'activities': 15, 'contingency': 10}
FALLBACKS = [
    CulturalCandidate(id='curated-theme', name='Campus Fusion', category='theme', tags=['campus']),
    CulturalCandidate(id='curated-music', name='Student mixed-genre playlist', category='music', tags=['music','campus']),
    CulturalCandidate(id='curated-activities', name='Interactive team quiz', category='activities', tags=['games','campus']),
    CulturalCandidate(id='curated-food', name='Vegetarian-friendly food stalls', category='food', tags=['vegetarian','campus']),
]

def tokens(text):
    return set(re.findall(r'[a-z0-9]+', text.lower()))

def rank(candidate, brief):
    audience = set().union(*(tokens(v) for v in brief.audience.interests))
    labels = tokens(candidate.name) | set().union(*(tokens(v) for v in candidate.tags))
    overlap = len(audience & labels) / max(1, len(audience))
    return round(min(1.0, .7 * candidate.score + .3 * overlap), 4)

def excluded(item, constraints):
    rules = ' '.join(constraints).lower()
    label = ' '.join([item.name, *item.tags]).lower()
    if any(t in rules for t in ['no alcohol','alcohol-free','alcohol free']):
        if any(t in label for t in ['alcohol','beer','wine','cocktail','liquor']): return True
    if any(t in rules for t in ['vegetarian only','pure veg','strict vegetarian']):
        if any(t in label for t in ['meat','chicken','fish','seafood','beef','pork']): return True
    if any(t in rules for t in ['no nuts','nut-free']):
        if any(t in label for t in ['peanut','almond','cashew','walnut']): return True
    return False

def allocation(budget):
    # Round first four allocations to cents; reserve remainder for contingency.
    cents = round(budget * 100)
    allocated = []
    remaining = cents
    for name, pct in list(WEIGHTS.items())[:-1]:
        part = round(cents * pct / 100)
        remaining -= part
        allocated.append(BudgetItem(category=name, amount=part/100,
                                    share_percent=part*100/cents))
    allocated.append(BudgetItem(category='contingency', amount=remaining/100,
                                share_percent=remaining*100/cents))
    return allocated

def generate_plan(brief: PlanRequest, candidates: list[CulturalCandidate] | None = None) -> PlanResponse:
    """Return a consistent event plan. Never fabricate Qloo evidence."""
    candidates = candidates or []
    picked = {}
    warnings = []
    for category in Category:
        available = [c for c in candidates if c.category == category and
                     c.id not in brief.rejected_ids and not excluded(c, brief.constraints)]
        available.sort(key=lambda c: (-rank(c, brief), c.id))
        selected = available[:1 if category == Category.theme else 2]
        if not selected:
            selected = [c for c in FALLBACKS if c.category == category and
                        c.id not in brief.rejected_ids and not excluded(c, brief.constraints)][:1]
            warnings.append(f'No eligible {category.value} provider results; curated fallback used.'
                            if selected else f'No eligible {category.value} results.')
        picked[category] = [Recommendation(
            id=c.id, name=c.name, category=c.category,
            reason=('Ranked by audience-interest overlap and supplied relevance score.'
                    if c.source == 'qloo' else 'Clearly labelled non-Qloo fallback.'),
            source=c.source, source_id=c.source_id,
            evidence=c.evidence if c.source == 'qloo' else None,
            rank_score=rank(c, brief)) for c in selected]
    sources = {r.source for category_results in picked.values() for r in category_results}
    status = ('none' if not sources else 'qloo' if sources == {'qloo'} else
              'mixed' if 'qloo' in sources else 'mock' if 'mock' in sources else 'curated')
    if brief.constraints:
        warnings.append('Organizer must manually verify constraints, allergens and accessibility.')
    if brief.currency == 'INR' and brief.budget / brief.attendees < 100:
        warnings.append('Under INR 100 per attendee: check feasibility.')
    theme = picked[Category.theme][0].name if picked[Category.theme] else brief.event_type
    return PlanResponse(plan=EventPlan(
        theme=theme, music=picked[Category.music], activities=picked[Category.activities],
        food=picked[Category.food], budget=allocation(brief.budget),
        total_budget=brief.budget, per_attendee=round(brief.budget/brief.attendees, 2),
        currency=brief.currency, warnings=warnings, evidence_status=status,
        audience_name=brief.audience.name))
