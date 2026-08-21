import json
import os
import requests

from app.outreach.prompts import OUTREACH_SYSTEM_PROMPT, build_outreach_prompt


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = os.getenv("OPENROUTER_MODEL", "liquid/lfm-2.5-2.6b:free")



def generate_outreach(creator):
    """
    Generate:

        1. Email subject
        2. Email body
        3. Instagram DM

    using the LLM.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found")

    prompt = build_outreach_prompt(creator)

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": OUTREACH_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)

    response.raise_for_status()

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    result = json.loads(content)

    required_fields = ["email_subject", "email_body", "instagram_dm"]

    for field in required_fields:
        if field not in result:
            raise ValueError(f"LLM response missing: {field}")

    return result
