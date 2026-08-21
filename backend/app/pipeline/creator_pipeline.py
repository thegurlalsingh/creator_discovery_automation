import json
import os
import time

from app.instagram.browser import InstagramBrowser
from app.outreach.generator import generate_outreach

from app.database.supabase import save_outreach_to_supabase

from app.discovery.influencer_discovery import discover_influencers

from app.instagram.reel_scraper import get_last_reel_data

from app.analysis.engagement import calculate_engagement_rate

from app.analysis.llm_analyzer import analyze_with_llm

from app.models.creator import Creator

from app.config.constants import NUMBER_OF_REELS

from app.database.supabase import save_creator_to_supabase, save_reels_to_supabase

from app.utils.cancellation import check_stop


OUTPUT_DIRECTORY = "output"


def save_creator_json(creator):
    """
    Save one creator to:

        output/<username>.json

    IMPORTANT:
    This is only a JSON backup.

    Failure here must NEVER stop the pipeline.
    """

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    filename = f"{creator.username}.json"

    filepath = os.path.join(OUTPUT_DIRECTORY, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(creator.to_dict(), file, indent=4, ensure_ascii=False)

    return filepath


def save_all_creators(creators):
    """
    Save all creators into:

        output/creators.json

    IMPORTANT:
    This is only a final JSON export.

    Failure here must NEVER stop the pipeline.
    """

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    filepath = os.path.join(OUTPUT_DIRECTORY, "creators.json")

    data = [creator.to_dict() for creator in creators]

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return filepath


def process_creator(page, profile):
    """
    Complete analysis of ONE creator.

    Flow:

        Profile
           ↓
        Reels
           ↓
        Engagement
           ↓
        OpenRouter
           ↓
        Creator object
    """

    username = profile["username"].strip().lstrip("@")

    followers = profile.get("followers")

    print("\n" + "=" * 70)

    print(f"PROCESSING CREATOR: @{username}")

    print("=" * 70)

    print("\n[1/4] Scraping reels...")

    reels = get_last_reel_data(page, username, NUMBER_OF_REELS)

    print(f"Reels scraped: {len(reels)}")

    print("\n[2/4] Calculating engagement...")

    engagement_rate = calculate_engagement_rate(followers, reels)

    if engagement_rate is not None:
        print(f"Engagement rate: {engagement_rate}%")

    else:
        print("Engagement rate: Not Found")

    print("\n[3/4] Running LLM analysis...")

    llm_result = analyze_with_llm(username, reels)

    print("\n[4/4] Building creator object...")

    creator = Creator(
        username=username,
        name=profile.get("name", "Not Found"),
        contact_email=profile.get("contact_email", "Not Found"),
        follower_count=followers,
        profile_url=profile.get("profile_url"),
        verified=profile.get("verified"),
        bio=profile.get("bio"),
        engagement_rate=(engagement_rate),
        category=llm_result.get("category", "Not Found"),
        content_themes=(llm_result.get("content_themes", [])),
    )

    return creator, reels


def run_pipeline(keywords=None, target_profiles=None):
    """
    Run the complete creator pipeline.

    IMPORTANT:

    Supabase = PRIMARY STORAGE

    JSON = BACKUP / EXPORT

    JSON failures must NEVER stop
    the Supabase pipeline.
    """

    print("\n" + "=" * 70)

    print("INSTAGRAM CREATOR PIPELINE")

    print("=" * 70)

    browser = InstagramBrowser()

    page = browser.start()

    creators = []

    try:
        profiles = discover_influencers(
            page, keywords=keywords, target_profiles=target_profiles
        )

        print("\n" + "=" * 70)

        print(f"DISCOVERY COMPLETE: {len(profiles)} creators")

        print("=" * 70)

        total = len(profiles)

        for index, (username, profile) in enumerate(profiles.items(), 1):
            check_stop()

            print("\n" + "#" * 70)

            print(f"CREATOR {index}/{total}")

            print("#" * 70)

            # Create a fresh isolated page context to avoid Instagram login block
            creator_page = browser.create_page()
            try:
                creator, reels = process_creator(creator_page, profile)
            except Exception as e:
                print(f"\n Failed to process @{username}: {e}")
                continue
            finally:
                if creator_page:
                    creator_page.close()

            creators.append(creator)

            creator_id = None
            try:
                print("\nSaving creator to Supabase...")

                creator_id = save_creator_to_supabase(creator)

                if creator_id:
                    print(f"Supabase creator saved: @{creator.username}")

                    print("Saving reels to Supabase...")

                    reels_success = save_reels_to_supabase(creator_id, reels)

                    if reels_success:
                        print(f"Supabase reels saved: {len(reels)}")

                    else:
                        print(f"Reels could not be saved for @{creator.username}")

                else:
                    print(
                        f"Creator was not saved, "
                        f"so reels will not be saved "
                        f"for @{creator.username}"
                    )

            except Exception as e:
                print(f"Supabase save failed for @{creator.username}: {e}")

            if creator_id:
                try:
                    print("\nGenerating email + Instagram DM...")

                    outreach = generate_outreach(creator)

                    print("\nEmail Subject:")

                    print(outreach["email_subject"])

                    print("\nInstagram DM:")

                    print(outreach["instagram_dm"])

                    save_outreach_to_supabase(creator_id, outreach)

                    print("Outreach saved to Supabase")

                except Exception as e:
                    print(f"Outreach failed for @{creator.username}: {e}")

            else:
                print("Skipping outreach because creator was not saved to Supabase.")

            try:
                filepath = save_creator_json(creator)

                print(f"JSON backup saved: {filepath}")

            except Exception as e:
                print(f"JSON backup failed for @{creator.username}: {e}")

            print(f"\nFinished @{creator.username}")

            time.sleep(0.5)

        print("\n" + "=" * 70)

        print("CREATOR PROCESSING COMPLETE")

        print("=" * 70)

        print(f"Creators processed: {len(creators)}")

        try:
            filepath = save_all_creators(creators)

            print(f"Combined JSON saved: {filepath}")

        except Exception as e:
            print(f"Combined JSON failed: {e}")

            print("Supabase data is unaffected.")

        print("\n========== FINAL DATA ==========\n")

        try:
            final_data = [creator.to_dict() for creator in creators]

            print(json.dumps(final_data, indent=4, ensure_ascii=False))

        except Exception as e:
            print(f"Could not print final JSON: {e}")

        print("\n" + "=" * 70)

        print("PIPELINE COMPLETE")

        print("=" * 70)

        print(f"Creators successfully processed: {len(creators)}")

        return creators

    finally:
        browser.close()
