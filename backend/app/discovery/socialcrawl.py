import requests
import uuid

from app.config.settings import SOCIALCRAWL_API_KEY, SOCIALCRAWL_BASE_URL


def get_headers():

    return {
        "x-api-key": SOCIALCRAWL_API_KEY,
        "Cache-Control": "no-cache",
        "Idempotency-Key": str(uuid.uuid4()),
    }


def search_profiles(keyword):

    url = f"{SOCIALCRAWL_BASE_URL}/instagram/search/profiles"

    params = {"query": keyword}

    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)

        response.raise_for_status()

        result = response.json()

        return result.get("data", {}).get("items", [])

    except requests.exceptions.RequestException as e:
        print(f"Search failed for '{keyword}': {e}")

        return []


def get_similar_profiles(username):

    url = f"{SOCIALCRAWL_BASE_URL}/instagram/similar"

    params = {"handle": username}

    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)

        response.raise_for_status()

        result = response.json()

        return result.get("data", {}).get("items", [])

    except requests.exceptions.RequestException as e:
        print(f"Similar search failed for @{username}: {e}")

        return []
