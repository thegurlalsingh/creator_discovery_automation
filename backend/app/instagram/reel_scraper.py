from bs4 import BeautifulSoup

from app.config.constants import INSTAGRAM_BASE_URL, NUMBER_OF_REELS
from urllib.parse import urlparse

from app.analysis.engagement import extract_engagement

from app.utils.cancellation import check_stop


def is_same_creator_reel(url, username):
    """
    Check whether a reel URL actually belongs
    to the requested Instagram username.
    """

    parsed = urlparse(url)

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        return False

    owner = parts[0]
    content_type = parts[1]

    return content_type == "reel" and owner.lower() == username.lower()


def extract_reel_description(soup):
    """
    Extract reel description from Instagram HTML.
    """

    meta_description = soup.find("meta", attrs={"name": "description"})

    if meta_description:
        content = meta_description.get("content")

        if content:
            return content.strip()

    og_description = soup.find("meta", attrs={"property": "og:description"})

    if og_description:
        content = og_description.get("content")

        if content:
            return content.strip()

    text = soup.get_text(" ", strip=True)

    if text:
        return text[:2000]

    return None


def get_last_reel_data(page, username, number_of_reels=NUMBER_OF_REELS):
    """
    Get latest reels for a creator.

    Returns:

        [
            {
                url,
                description,
                likes,
                comments
            }
        ]
    """

    username = username.strip().lstrip("@")

    profile_url = f"{INSTAGRAM_BASE_URL}/{username}/"

    try:
        print(f"\nOpening: {profile_url}")

        page.goto(profile_url, wait_until="domcontentloaded", timeout=90_000)

        page.wait_for_timeout(9000)

        links = page.locator("a").all()

        reel_urls = []

        for link in links:
            href = link.get_attribute("href")

            if not href:
                continue

            if "/reel/" not in href:
                continue

            if href.startswith("/"):
                href = INSTAGRAM_BASE_URL + href

            if href not in reel_urls:
                reel_urls.append(href)

            if len(reel_urls) >= number_of_reels:
                break

        print(f"\nReel URLs found: {len(reel_urls)}")

        for url in reel_urls:
            print(url)

        reels = []

        for index, reel_url in enumerate(reel_urls, 1):
            check_stop()

            print(f"\n{'=' * 70}")

            print(f"REEL {index}/{number_of_reels}")

            print(f"Opening: {reel_url}")

            page.goto(reel_url, wait_until="domcontentloaded", timeout=30_000)

            page.wait_for_timeout(2000)

            html = page.content()

            soup = BeautifulSoup(html, "html.parser")

            description = extract_reel_description(soup)

            engagement = extract_engagement(description)

            reel = {
                "url": reel_url,
                "description": description,
                "likes": engagement["likes"],
                "comments": engagement["comments"],
            }

            reels.append(reel)

            print("\nRAW DESCRIPTION:")

            print(description if description else "NOT FOUND")

            print(f"\nLikes: {engagement['likes']:,}")

            print(f"Comments: {engagement['comments']:,}")

        return reels

    except Exception as e:
        print(f"\nReel scraping failed for @{username}: {e}")

        return []
