"""Day 1 deterministic agent; Qloo candidates are injected by Avik's integration."""
import re
from decimal import Decimal, ROUND_HALF_UP
from .schemas import (Category, CulturalCandidate, Recommendation,
                      BudgetItem, BudgetEstimate, QlooEvidence, PlanRequest, PlanResponse)

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
    # Largest remainder allocation preserves the exact total, even for tiny budgets.
    cents = int((Decimal(str(budget)) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    if cents < 1:
        raise ValueError('Budget must be at least INR 0.01')
    shares = [(name, cents * pct // 100, cents * pct % 100) for name, pct in WEIGHTS.items()]
    remaining = cents - sum(part for _, part, _ in shares)
    bonuses = set(sorted(range(len(shares)), key=lambda i: (-shares[i][2], i))[:remaining])
    return [BudgetItem(category=name, amount=(part + (i in bonuses)) / 100,
                       share_percent=(part + (i in bonuses)) * 100 / cents)
            for i, (name, part, _) in enumerate(shares)]


def recommendation(candidate, brief):
    return Recommendation(
        id=candidate.id, title=candidate.name, category=candidate.category,
        reason=('Ranked by audience-interest overlap and supplied relevance score.'
                if candidate.source == 'qloo' else
                'Mock candidate; not Qloo evidence.' if candidate.source == 'mock' else
                'Curated suggestion; not Qloo evidence.'),
        source=candidate.source,
        qloo_evidence=(QlooEvidence(source_id=candidate.source_id, signal=candidate.evidence)
                       if candidate.source == 'qloo' else None),
        rank_score=rank(candidate, brief))


def generate_plan(brief: PlanRequest, candidates: list[CulturalCandidate] | None = None) -> PlanResponse:
    """Consume normalized candidates; never invent cultural evidence or prices."""
    candidates = candidates or []
    picked, alternatives, warnings = {}, [], []
    seen = set()
    unique = []
    for candidate in candidates:
        if candidate.id not in seen:
            unique.append(candidate)
            seen.add(candidate.id)
    for category in Category:
        available = [c for c in unique if c.category == category and
                     c.id not in brief.rejected_ids and not excluded(c, brief.constraints)]
        available.sort(key=lambda c: (-rank(c, brief), c.id))
        count = 1 if category == Category.theme else 2
        selected = available[:count]
        alternatives.extend(recommendation(c, brief) for c in available[count:count + 2])
        if not selected:
            selected = [c for c in FALLBACKS if c.category == category and
                        c.id not in brief.rejected_ids and not excluded(c, brief.constraints)][:1]
            warnings.append(f'No eligible {category.value} provider results; curated fallback used.'
                            if selected else f'No eligible {category.value} results.')
        picked[category] = [recommendation(c, brief) for c in selected]
    results = [r for rows in picked.values() for r in rows]
    sources = {r.source for r in results}
    status = ('none' if not sources else 'qloo' if sources == {'qloo'} else
              'mixed' if 'qloo' in sources else 'mock' if 'mock' in sources else 'curated')
    if brief.constraints:
        warnings.append('Organizer must manually verify constraints, allergens and accessibility.')
    if brief.budget_per_person < 100:
        warnings.append('Under INR 100 per attendee: check feasibility.')
    warnings.append('LLM baseline and comparison are not implemented yet.')
    total = Decimal(str(brief.budget_per_person)) * brief.attendees
    theme = picked[Category.theme][0].title if picked[Category.theme] else brief.audience.event_type
    return PlanResponse(
        title=f'{theme} — {brief.audience.event_type}', theme=theme,
        recommendations=results, alternatives=alternatives,
        budget_estimate=BudgetEstimate(
            breakdown=allocation(total), total=float(total),
            budget_per_person=brief.budget_per_person, attendees=brief.attendees,
            currency=brief.currency,
            assumptions=[
                'Total allocation = budget_per_person × attendees; currency INR.',
                'Estimated allocations, not verified vendor prices or quotations.',
                'Venue 30%, food 25%, production 20%, activities 15%, contingency 10%; rounded to paise.',
                'Campus venue is not assumed free; any savings require organizer confirmation.',
                'Taxes, permits, travel and supplier availability are not independently verified.',
            ]),
        warnings=warnings, evidence_status=status, audience_name=brief.audience.name)
