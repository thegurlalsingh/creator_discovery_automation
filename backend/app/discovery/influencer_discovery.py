import time

from app.discovery.socialcrawl import search_profiles, get_similar_profiles

from app.instagram.profile_scraper import scrape_instagram_profile

from app.config.constants import MIN_FOLLOWERS, MAX_FOLLOWERS, TARGET_PROFILES, KEYWORDS

from app.utils.helpers import is_valid_follower_count

from app.utils.cancellation import check_stop


def discover_influencers(page, keywords=None, target_profiles=None):
    """
    Discover creators using:

        1. Keyword search
        2. Similar account expansion
        3. Instagram follower verification

    Returns:

        {
            username: profile_data
        }
    """

    if keywords is None:
        keywords = KEYWORDS
    if target_profiles is None:
        target_profiles = TARGET_PROFILES

    good_profiles = {}

    similar_profiles = set()

    print("\n========== KEYWORD SEARCH ==========\n")

    for keyword in keywords:
        check_stop()

        if len(good_profiles) >= target_profiles:
            break

        print(f"Searching keyword: {keyword}")

        profiles = search_profiles(keyword)

        print(f"Profiles returned: {len(profiles)}")

        for item in profiles:
            check_stop()

            author = item.get("author", {})

            username = author.get("username")

            followers = author.get("followers")

            if not username:
                continue

            if is_valid_follower_count(followers, MIN_FOLLOWERS, MAX_FOLLOWERS):
                if username not in good_profiles:
                    good_profiles[username] = {
                        "username": username,
                        "name": author.get("display_name"),
                        "contact_email": "Not Found",
                        "followers": followers,
                        "verified": author.get("verified"),
                        "profile_url": (
                            author.get("url")
                            or f"https://www.instagram.com/{username}/"
                        ),
                        "bio": author.get("bio"),
                    }

                    print(f"  + Added: @{username} ({followers:,} followers)")

            if len(good_profiles) >= target_profiles:
                break

        print(f"Current valid profiles: {len(good_profiles)}/{target_profiles}")

        time.sleep(0.5)

    print("\n========== SIMILAR ACCOUNT EXPANSION ==========\n")

    if len(good_profiles) < target_profiles:
        print(f"Only found {len(good_profiles)} profiles.")

        print("Expanding using similar accounts...")

        seed_profiles = list(good_profiles.keys())

        for username in seed_profiles:
            check_stop()

            print(f"\nFinding accounts similar to @{username}")

            profiles = get_similar_profiles(username)

            print(f"Similar profiles returned: {len(profiles)}")

            for item in profiles:
                author = item.get("author", {})

                similar_username = author.get("username")

                if not similar_username:
                    continue

                if similar_username in good_profiles:
                    continue

                similar_profiles.add(similar_username)

            time.sleep(0.5)

    print("\n========== SCRAPING SIMILAR PROFILES ==========\n")

    print(f"Unique similar profiles found: {len(similar_profiles)}")

    total_similar = len(similar_profiles)

    for index, username in enumerate(similar_profiles, 1):
        check_stop()

        if len(good_profiles) >= target_profiles:
            break

        print(f"\n[{index}/{total_similar}] Checking @{username}")

        profile = scrape_instagram_profile(page, username)

        if profile is None:
            print(f"  X Could not scrape @{username}")

            continue

        followers = profile.get("followers")

        if followers is None:
            print(f"  X Could not find follower count for @{username}")

            continue

        print(f"  Followers: {followers:,}")

        print(f"  Name: {profile['name']}")

        print(f"  Email: {profile['contact_email']}")

        if not is_valid_follower_count(followers, MIN_FOLLOWERS, MAX_FOLLOWERS):
            print(f"  X Rejected @{username}")

            continue

        good_profiles[username] = profile

        print(f"  + Added @{username}")

        print(f"  Current total: {len(good_profiles)}/{target_profiles}")

        time.sleep(0.5)

    print("\n========== ENRICHING KEYWORD PROFILES ==========\n")

    for username, profile in good_profiles.items():
        check_stop()

        if profile.get("contact_email") != "Not Found":
            continue

        print(f"\nEnriching @{username}")

        enriched = scrape_instagram_profile(page, username, profile.get("name"))

        if enriched:
            profile["name"] = enriched["name"]

            profile["contact_email"] = enriched["contact_email"]

            profile["profile_url"] = enriched["profile_url"]

            print(f"  Name: {profile['name']}")

            print(f"  Email: {profile['contact_email']}")

        time.sleep(0.5)

    print("\n========== DISCOVERY COMPLETE ==========\n")

    print(f"Total influencers found: {len(good_profiles)}")

    return good_profiles
