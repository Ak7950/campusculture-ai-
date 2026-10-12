import os
from typing import Any, Mapping

import httpx

from app.config import get_qloo_api_key


class QlooAPIError(RuntimeError):
    """Raised when a Qloo API request fails."""


async def get_insights(
    params: Mapping[str, str | int],
) -> dict[str, Any]:
    api_key = get_qloo_api_key()

    base_url = os.getenv(
        "QLOO_BASE_URL",
        "https://hackathon.api.qloo.com",
    ).rstrip("/")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{base_url}/v2/insights",
                headers={
                    "X-Api-Key": api_key,
                    "Accept": "application/json",
                },
                params=params,
            )

    except httpx.TimeoutException as exc:
        raise QlooAPIError("Qloo request timed out.") from exc
    except httpx.RequestError as exc:
        raise QlooAPIError(
            "Could not connect to the Qloo API."
        ) from exc

    if response.is_error:
        raise QlooAPIError(
            f"Qloo returned HTTP {response.status_code}: "
            f"{response.text[:300]}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise QlooAPIError(
            "Qloo returned an invalid JSON response."
        ) from exc

    if not isinstance(data, dict):
        raise QlooAPIError(
            "Qloo returned an unexpected response format."
        )

    return data
