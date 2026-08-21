import json

from app.instagram.reel_scraper import get_last_5_reel_descriptions

from app.analysis.engagement import (
    calculate_engagement_rate,
    is_suspicious_engagement_rate,
)

from app.analysis.llm_analyzer import analyze_with_llm

from app.database.creator_repo import CreatorRepository


def process_creator(creator):
    """
    Process one creator completely.

    Steps:

    1. Scrape reels
    2. Calculate engagement
    3. Analyze content using LLM
    4. Build final creator object
    5. Save creator + reels to Supabase
    """

    username = creator["username"].strip().lstrip("@")

    print("\n" + "=" * 70)

    print(f"PROCESSING CREATOR: @{username}")

    print("=" * 70)

    print("\n[1/5] Scraping reels...")

    reels = get_last_5_reel_descriptions(username)

    print(f"Reels scraped: {len(reels)}")

    print("\n[2/5] Calculating engagement...")

    engagement_rate = calculate_engagement_rate(creator["follower_count"], reels)

    if engagement_rate is None:
        print("Engagement rate: Not Found")

    else:
        print(f"Engagement rate: {engagement_rate}%")

        if is_suspicious_engagement_rate(engagement_rate):
            print("WARNING: Engagement rate is unusually high.")

    print("\n[3/5] Running LLM analysis...")

    llm_result = analyze_with_llm(username, reels)

    print("\n[4/5] Building creator JSON...")

    final_creator = {
        "username": username,
        "name": creator.get("name"),
        "contact_email": creator.get("contact_email"),
        "follower_count": creator.get("follower_count"),
        "profile_url": creator.get("profile_url"),
        "verified": creator.get("verified", False),
        "bio": creator.get("bio"),
        "engagement_rate": engagement_rate,
        "category": llm_result.get("category"),
        "content_themes": llm_result.get("content_themes", []),
    }

    print("\n[5/5] Saving to Supabase...")

    try:
        database_result = CreatorRepository.save_creator(final_creator, reels)

        print("Creator saved to Supabase.")

        print(f"Creator ID: {database_result['creator']['id']}")

        print(f"Reels saved: {len(database_result['reels'])}")

    except Exception as e:
        print(f"Supabase save failed: {e}")

        database_result = None

    return {"creator": final_creator, "reels": reels, "database": database_result}
