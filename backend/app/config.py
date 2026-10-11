import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_qloo_api_key() -> str:
    api_key = os.getenv("QLOO_API_KEY", "").strip()

    if not api_key or api_key == "your_qloo_api_key_here":
        raise RuntimeError(
            "QLOO_API_KEY is missing. Add your key to the project-root .env file."
        )

    return api_key
