# CampusCulture agent — Day 1 architecture

**API contract proposal:** Avik and Humza must confirm this before merging. Implementation uses Pydantic v2.

## `POST /api/plan`

Request body:

```json
{"audience":{"name":"Indie music society","interests":["indie music","art"]},"event_type":"music night","location":"Patiala","attendees":120,"budget":60000,"currency":"INR","constraints":["No alcohol"],"rejected_ids":[]}
```

Response is `PlanResponse`: `plan`, `baseline: null`, `comparison: null` (Day 2 will implement the comparison). `plan` provides `theme`, `music[]`, `activities[]`, `food[]`, `budget[]`, `total_budget`, `per_attendee`, `currency`, `warnings`, `evidence_status`, and `audience_name`.

## Integration

1. Avik validates the request with `PlanRequest` and fetches Qloo insights.
2. Avik normalizes API data to `CulturalCandidate(id, name, category, score, tags, source='qloo', source_id, evidence)`. Scores are app-normalized `[0,1]`, **not asserted to be raw Qloo scores**.
3. Avik calls `generate_plan(brief, candidates)` and returns `response.model_dump(mode='json')`.
4. Humza renders recommendations, source labels, evidence, warnings and budget. Rejection appends an ID to `rejected_ids` and resends the request.

## Ranking and constraints

- Score = 70% provided normalized relevance + 30% overlap with audience-interest tokens. Deterministic tie-break by candidate ID.
- Choose one theme and at most two results for each other category.
- No Qloo results => curated fallback with explicit source attribution. Never fabricate affinity evidence.
- Basic exclusions for alcohol, certain meat terms, nuts. The output warns that allergens/accessibility require organizer review. These rules do not guarantee safety.
- Budget: 30% venue, 25% food, 20% production, 15% activities, 10% contingency. Sum rounded to cents; these are estimated allocations, not quotations.

## Day 2 pending

Real Qloo retrieval, FastAPI route, LLM-generated coherent narrative, generic LLM baseline, comparative metrics, full revision logic and deployment. No part of Day 1 claims these are already integrated.

## Tests

From `backend/`, with `pydantic>=2` and `pytest` installed: `python -m pytest -q`. Three sample audience briefs are in `backend/tests/sample_profiles.json`.
