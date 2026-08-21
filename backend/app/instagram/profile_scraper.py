import re

from bs4 import BeautifulSoup

from app.config.constants import INSTAGRAM_BASE_URL

from app.utils.helpers import convert_number, extract_followers_from_text


def extract_name_and_email(soup, html, fallback_name=None):
    """
    Extract:

        name
        contact_email

    Email defaults to "Not Found".
    """

    name = None
    email = None

    og_title = soup.find("meta", attrs={"property": "og:title"})

    if og_title:
        content = og_title.get("content", "").strip()

        if content:
            match = re.search(r"^(.*?)\s*\(@[A-Za-z0-9._]+\)", content)

            if match:
                extracted_name = match.group(1).strip()

                if extracted_name:
                    name = extracted_name

    if not name:
        meta_description = soup.find("meta", attrs={"name": "description"})

        if meta_description:
            content = meta_description.get("content", "").strip()

            if content:
                match = re.search(r"^(.*?)\s*\(@[A-Za-z0-9._]+\)", content)

                if match:
                    extracted_name = match.group(1).strip()

                    if extracted_name:
                        name = extracted_name

    text = soup.get_text(" ", strip=True)

    for link in soup.find_all("a", href=True):
        href = link.get("href", "")

        if href.lower().startswith("mailto:"):
            possible_email = href[7:].split("?")[0].strip()

            if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", possible_email):
                email = possible_email

                break

    if not email:
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            html,
        )

        if email_match:
            email = email_match.group(0).strip()

    if not email:
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )

        if email_match:
            email = email_match.group(0).strip()

    if not name:
        name = fallback_name if fallback_name else "Not Found"

    if not email:
        email = "Not Found"

    return {"name": name, "contact_email": email}


def scrape_instagram_profile(page, username, fallback_name=None):
    """
    Scrape an Instagram profile.

    Returns:

        {
            name,
            contact_email,
            followers,
            profile_url,
            bio
        }
    """

    username = username.strip().lstrip("@")

    url = f"{INSTAGRAM_BASE_URL}/{username}/"

    try:
        print(f"  Opening: {url}")

        page.goto(url, wait_until="domcontentloaded", timeout=30_000)

        page.wait_for_timeout(2500)

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")

        followers = None

        for meta in soup.find_all("meta"):
            content = meta.get("content", "")

            followers = extract_followers_from_text(content)

            if followers is not None:
                break

        if followers is None:
            text = soup.get_text(" ", strip=True)

            followers = extract_followers_from_text(text)

        if followers is None:
            followers = extract_followers_from_text(html)

        profile_info = extract_name_and_email(soup, html, fallback_name)

        bio = None

        meta_description = soup.find("meta", attrs={"name": "description"})

        if meta_description:
            content = meta_description.get("content")

            if content:
                bio = content.strip()

        return {
            "username": username,
            "name": profile_info["name"],
            "contact_email": profile_info["contact_email"],
            "followers": followers,
            "profile_url": url,
            "bio": bio,
        }

    except Exception as e:
        print(f"  Scraping failed for @{username}: {e}")

        return None
