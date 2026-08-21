import re

from app.utils.helpers import convert_number


def extract_engagement(description):
    """
    Extract likes and comments from an Instagram
    reel description.

    Example:

        46K likes, 3,365 comments - nextforai...

    Returns:

        {
            "likes": 46000,
            "comments": 3365
        }
    """

    if not description:
        return {"likes": 0, "comments": 0}

    likes_match = re.search(
        r"([\d,.]+)\s*(K|M|B)?\s+likes?", description, re.IGNORECASE
    )

    comments_match = re.search(
        r"([\d,.]+)\s*(K|M|B)?\s+comments?", description, re.IGNORECASE
    )

    likes = 0

    comments = 0

    if likes_match:
        likes = convert_number(likes_match.group(1), likes_match.group(2))

    if comments_match:
        comments = convert_number(comments_match.group(1), comments_match.group(2))

    return {"likes": likes, "comments": comments}


def calculate_engagement_rate(followers, reels):
    """
    Calculate average engagement rate.

    Formula:

        average(likes + comments)
        ------------------------- × 100
              followers
    """

    if not followers or not reels:
        return None

    total_engagement = 0

    valid_reels = 0

    for reel in reels:
        likes = reel.get("likes", 0)

        comments = reel.get("comments", 0)

        if likes == 0 and comments == 0:
            continue

        total_engagement += likes + comments

        valid_reels += 1

    if valid_reels == 0:
        return None

    average_engagement = total_engagement / valid_reels

    engagement_rate = (average_engagement / followers) * 100

    return round(engagement_rate, 2)
