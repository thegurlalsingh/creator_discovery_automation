import json
import requests
import re

from app.config.settings import OPENROUTER_API_KEY

from app.config.constants import OPENROUTER_URL, OPENROUTER_MODEL


def parse_json_response(content):
    """
    Convert the LLM response into a Python dictionary.

    Handles:

        pure JSON

    and:

        ```json
        {...}
        ```
    """

    if not content:
        return None

    content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        pass

    match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL | re.IGNORECASE)

    if match:
        try:
            return json.loads(match.group(1))

        except json.JSONDecodeError:
            pass

    match = re.search(r"```\s*(.*?)\s*```", content, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(1))

        except json.JSONDecodeError:
            pass

    start = content.find("{")

    end = content.rfind("}")

    if start != -1 and end != -1 and end > start:
        json_text = content[start : end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError:
            pass

    return None


def analyze_with_llm(username, reels):
    """
    Analyze the creator's reels using OpenRouter.

    Returns:

        {
            "category": "...",
            "content_themes": [...]
        }
    """
    if not reels:
        print("\nNo reels available. Skipping LLM analysis.")

        return {"category": None, "content_themes": []}

    reel_text = ""

    for index, reel in enumerate(reels, 1):
        reel_text += f"""

REEL {index}

Caption:
{reel.get("description", "")}

Likes:
{reel.get("likes", 0)}

Comments:
{reel.get("comments", 0)}

----------------------------------------
"""

    prompt = f"""
You are analyzing the Instagram creator @{username}.

Below are the creator's latest Instagram reels.

Use ONLY the provided information.

Determine:

1. Category / Niche
2. Content Themes

CATEGORY / NICHE:
Return ONE concise high-level category.

CONTENT THEMES:
Return 3 to 6 recurring themes that are clearly
supported by the reel captions and hashtags.

Do NOT invent information.

Do NOT include:
- follower count
- engagement rate
- name
- email
- URLs

Return ONLY valid JSON.

Expected format:

{{
    "category": "Artificial Intelligence & Technology",
    "content_themes": [
        "AI News",
        "AI Safety",
        "Future of Technology"
    ]
}}

REEL DATA:

{reel_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "reasoning": {"enabled": True},
    }

    try:
        response = requests.post(
            OPENROUTER_URL, headers=headers, json=payload, timeout=60
        )

        response.raise_for_status()

        result = response.json()

        content = result["choices"][0]["message"].get("content")

        print("\n========== RAW LLM RESPONSE ==========\n")

        print(content)

        llm_data = parse_json_response(content)

        if not llm_data:
            print("\nLLM returned invalid JSON.")

            return {"category": "Not Found", "content_themes": []}

        category = llm_data.get("category", "Not Found")

        content_themes = llm_data.get("content_themes", [])

        if not isinstance(content_themes, list):
            content_themes = []

        return {"category": category, "content_themes": content_themes}

    except requests.exceptions.RequestException as e:
        print(f"\nOpenRouter request failed: {e}")

        return {"category": "Not Found", "content_themes": []}

    except (KeyError, IndexError, TypeError) as e:
        print(f"\nUnexpected OpenRouter response: {e}")

        print(result if "result" in locals() else "No response")

        return {"category": "Not Found", "content_themes": []}
