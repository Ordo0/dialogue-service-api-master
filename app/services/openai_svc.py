import requests
from app.core.config import settings


def generate_openai_prompt(prompt: str) -> str:
    with requests.Session as session:
        response = session.get(
            url=settings.OPENAI_URL,
            params={'prompt': prompt}
        )

        result = response.json()

    return result['message']
