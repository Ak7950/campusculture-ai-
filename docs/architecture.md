# CampusCulture agent integration contract

This revision implements the team-supplied request contract and the response fields
listed below. Avik and Humza should use these exact field names for integration.
Pydantic v2; only INR is supported in this MVP.

## POST /api/plan

```json
{
  "audience": {
    "interests": ["indie music", "anime"],
    "location": "Chandigarh",
    "event_type": "campus social"
  },
  "budget_per_person": 500,
  "attendees": 100,
  "constraints": ["campus venue"]
}
```

Optional fields: `audience.name` (default `Primary audience`), `currency`
(default `INR`), `constraints` (default `[]`), `rejected_ids` (default `[]`).
Attendees must be a positive JSON integer. Budget must be finite and at least
INR 0.01, with at most two decimal places. Unknown fields are rejected.
Old top-level `budget`, `location` and `event_type` are deliberately not accepted.

## Response: PlanResponse

| Field | Shape |
| --- | --- |
| title, theme | Strings |
| recommendations | Array of recommendation objects across theme/music/activities/food |
| budget_estimate | breakdown, total, budget_per_person, attendees, currency, assumptions |
| alternatives | Array of eligible recommendations not selected for the main plan |
| baseline | Same EventPlan structure, or null until an LLM baseline is implemented |
| comparison | criteria[], observations[], limitations[], or null until evaluated |
| warnings | String array |
| evidence_status | qloo, mixed, mock, curated, none; based on selected recommendations |
| audience_name | String |

Each recommendation contains `id`, `category`, `title`, `reason`, `source`,
`qloo_evidence` and `rank_score`. `qloo_evidence` is null for curated/mock items;
for Qloo it is `{ "source_id": "actual-provider-id", "signal": null }` or an
actual supplied signal string. `rank_score` is application-defined, never a raw
Qloo affinity or proof of cultural preference. A source ID identifies the
retrieved entity; it alone does not prove an audience affinity.

## Backend integration (Avik)

1. Validate the body with `PlanRequest`.
2. Resolve `request.audience.interests` and retrieve actual Qloo results.
3. Normalize each result into `CulturalCandidate(id, name, category, score,
   tags, source='qloo', source_id, evidence)`; retain actual provider identifiers
   and evidence, never model-generated claims. Score is normalized to [0,1].
4. Call `generate_plan(request, candidates)` and return its `PlanResponse`.
   With FastAPI, use `response_model=PlanResponse`.
5. Qloo errors belong to the backend. If it intentionally continues with empty
   candidates, append an explicit warning identifying the unavailable provider.

The internal candidate structure remains compatible with Day 1. Candidates are
not accepted in the public request body. Qloo candidates require a source ID.
The agent uses deterministic ranking and can run without API keys.

## Frontend integration (Humza)

Read `response.recommendations`, not `response.plan.music`. Group cards by
`category`; render `title`, `reason`, source labels and evidence separately.
Display budget assumptions beside the estimate. Do not label curated/mock
results as Qloo-powered. Show baseline/comparison as unavailable when null.
For rejection, append the recommendation ID to `rejected_ids` and resend the
same request. Audience switching sends a new request to the same endpoint.

## Planning, revisions and estimates

- Rank = 70% supplied normalized score + 30% audience-interest token overlap;
  ties break by ID. Duplicate candidate IDs are discarded after the first.
- Select one theme and at most two recommendations per other category.
  Return up to two remaining candidates per category as alternatives.
- Rejected and constraint-filtered items cannot appear in either list.
  If no eligible provider candidates remain, use labelled curated fallbacks.
- Constraint filters are basic keyword checks for alcohol, meat and nuts;
  they do not verify arbitrary requirements, allergens or accessibility.
- Total allocation = budget_per_person × attendees. Split venue 30%, food 25%,
  production 20%, activities 15%, contingency 10%, using largest remainders
  to preserve the exact total in paise even for very small budgets.
- These are allocation estimates, not vendor quotations. A campus venue is
  not assumed free. Taxes, permits and availability are unverified.

## Still pending

Actual Qloo retrieval and FastAPI endpoint belong to Avik. LLM narrative,
independent generic LLM-only baseline and comparative evaluation remain Day 2
work. Baseline must receive the same brief and constraints but no Qloo inputs.
No performance or personalization superiority is asserted by this revision.

## Verification

From backend/: `python -m pip install -r requirements.txt pytest`, then
`python -m pytest -q`. Tests cover contract round trips, sample audiences,
invalid inputs, evidence attribution, rejection/alternatives and exact budgets.
