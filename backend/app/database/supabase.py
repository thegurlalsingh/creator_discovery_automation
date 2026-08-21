import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is not set in .env")


if not SUPABASE_SECRET_KEY:
    raise ValueError("SUPABASE_KEY is not set in .env")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)



def save_creator_to_supabase(creator):
    """
    Insert or update creator in Supabase.

    Returns:
        creator_id if successful
        None if failed
    """

    data = {
        "username": creator.username,
        "name": creator.name,
        "contact_email": creator.contact_email,
        "follower_count": creator.follower_count,
        "profile_url": creator.profile_url,
        "verified": creator.verified,
        "bio": creator.bio,
        "engagement_rate": creator.engagement_rate,
        "category": creator.category,
        "content_themes": creator.content_themes,
    }

    try:
        response = (
            supabase.table("creators").upsert(data, on_conflict="username").execute()
        )

        if not response.data:
            print(f"No creator data returned for @{creator.username}")

            return None

        creator_id = response.data[0]["id"]

        return creator_id

    except Exception as e:
        print(f"Error saving creator @{creator.username}: {e}")

        return None



def save_reels_to_supabase(creator_id, reels):
    """
    Save reels belonging to a creator.

    creator_id:
        Primary key from creators table.

    reels:
        List returned by get_last_reel_data().
    """

    if not creator_id:
        print("Cannot save reels: creator_id is missing.")

        return False

    if not reels:
        print("No reels to save.")

        return True

    reel_rows = []

    for reel in reels:
        instagram_url = reel.get("url")

        if not instagram_url:
            continue

        reel_rows.append(
            {
                "creator_id": creator_id,
                "instagram_url": instagram_url,
                "description": reel.get("description"),
                "likes": reel.get("likes", 0),
                "comments": reel.get("comments", 0),
            }
        )

    if not reel_rows:
        print("No valid reels found.")

        return True

    try:
        response = (
            supabase.table("reels")
            .upsert(reel_rows, on_conflict=("creator_id,instagram_url"))
            .execute()
        )

        print(f"Saved {len(response.data)} reels")

        return True

    except Exception as e:
        print(f"Error saving reels: {e}")

        return False


def save_outreach_to_supabase(creator_id, outreach):

    data = {
        "creator_id": creator_id,
        "email_subject": outreach.get("email_subject"),
        "email_body": outreach.get("email_body"),
        "email_status": "generated",
        "instagram_dm": outreach.get("instagram_dm"),
        "instagram_dm_status": "generated",
    }

    response = (
        supabase.table("outreach").upsert(data, on_conflict="creator_id").execute()
    )

    return response.data
