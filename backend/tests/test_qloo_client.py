import asyncio

import httpx
import pytest
import respx

from app.qloo_client import QlooAPIError, get_insights
from app.config import get_qloo_api_key


BASE_URL = "https://hackathon.api.qloo.com"


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("QLOO_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="QLOO_API_KEY is missing"):
        asyncio.run(get_insights({}))


@respx.mock
def test_successful_insights_response(monkeypatch):
    monkeypatch.setenv("QLOO_API_KEY", "test-key")
    route = respx.get(f"{BASE_URL}/v2/insights").mock(
        return_value=httpx.Response(
            200,
            json={"results": {"entities": []}},
        )
    )

    result = asyncio.run(get_insights({"type": "urn:entity:artist"}))

    assert result == {"results": {"entities": []}}
    assert route.called


@respx.mock
def test_http_error(monkeypatch):
    monkeypatch.setenv("QLOO_API_KEY", "test-key")
    respx.get(f"{BASE_URL}/v2/insights").mock(
        return_value=httpx.Response(401, text="Unauthorized")
    )

    with pytest.raises(QlooAPIError, match="HTTP 401"):
        asyncio.run(get_insights({}))
