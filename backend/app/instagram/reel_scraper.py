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


def get_last_reel_data(
    page,
    username,
    number_of_reels=NUMBER_OF_REELS
):
    """
    Get latest reels for a creator.
    """

    username = username.strip().lstrip("@")

    profile_url = (
        f"{INSTAGRAM_BASE_URL}/{username}/"
    )

    try:

        print(
            f"\nOpening: {profile_url}"
        )

        # ====================================================
        # OPEN PROFILE
        # ====================================================

        try:

            page.goto(
                profile_url,
                wait_until="commit",
                timeout=30_000
            )

        except Exception as e:

            print(
                f"Navigation warning: {e}"
            )

        # Give Instagram time to render
        page.wait_for_timeout(5000)

        print(
            f"Current URL: {page.url}"
        )

        # ====================================================
        # WAIT FOR REEL LINKS
        # ====================================================

        try:

            page.wait_for_selector(
                "a[href*='/reel/']",
                timeout=15_000
            )

            print(
                "Reel elements detected."
            )

        except Exception:

            print(
                "Reel selector not found yet."
            )

        # ====================================================
        # SCROLL
        # ====================================================

        for _ in range(3):

            page.mouse.wheel(
                0,
                1000
            )

            page.wait_for_timeout(
                1500
            )

        # ====================================================
        # COLLECT REEL LINKS
        # ====================================================

        links = page.locator(
            "a[href*='/reel/']"
        ).all()

        reel_urls = []

        for link in links:

            href = link.get_attribute(
                "href"
            )

            if not href:
                continue

            if "/reel/" not in href:
                continue

            if href.startswith("/"):
                href = (
                    INSTAGRAM_BASE_URL
                    + href
                )

            if href not in reel_urls:

                reel_urls.append(
                    href
                )

            if (
                len(reel_urls)
                >= number_of_reels
            ):
                break

        print(
            f"\nReel URLs found: "
            f"{len(reel_urls)}"
        )

        for url in reel_urls:

            print(url)

        # ====================================================
        # SCRAPE EACH REEL
        # ====================================================

        reels = []

        for index, reel_url in enumerate(
            reel_urls,
            1
        ):

            check_stop()

            print(
                "\n"
                + "=" * 70
            )

            print(
                f"REEL "
                f"{index}/{len(reel_urls)}"
            )

            print(
                f"Opening: {reel_url}"
            )

            try:

                page.goto(
                    reel_url,
                    wait_until="commit",
                    timeout=30_000
                )

            except Exception as e:

                print(
                    f"Reel navigation warning: "
                    f"{e}"
                )

            page.wait_for_timeout(
                3000
            )

            html = page.content()

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            description = (
                extract_reel_description(
                    soup
                )
            )

            engagement = extract_engagement(
                description
            )

            reel = {

                "url": reel_url,

                "description":
                    description,

                "likes":
                    engagement["likes"],

                "comments":
                    engagement["comments"]
            }

            reels.append(
                reel
            )

            print(
                "\nRAW DESCRIPTION:"
            )

            print(
                description
                if description
                else "NOT FOUND"
            )

            print(
                f"\nLikes: "
                f"{engagement['likes']:,}"
            )

            print(
                f"Comments: "
                f"{engagement['comments']:,}"
            )

        return reels

    except Exception as e:

        print(
            f"\nReel scraping failed "
            f"for @{username}: {e}"
        )

        return []
