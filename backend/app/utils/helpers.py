import re


def convert_number(number, suffix=None):
    """
    Convert Instagram-style numbers into integers.

    Examples:

        46K      -> 46000
        61K      -> 61000
        3,365    -> 3365
        1.2M     -> 1200000
        2B       -> 2000000000
    """

    if not number:
        return 0

    number = number.replace(",", "").strip()

    value = float(number)

    if suffix:
        suffix = suffix.upper()

        if suffix == "K":
            value *= 1_000

        elif suffix == "M":
            value *= 1_000_000

        elif suffix == "B":
            value *= 1_000_000_000

    return int(value)


def is_valid_follower_count(followers, minimum, maximum):

    if followers is None:
        return False

    return minimum <= followers <= maximum


def extract_followers_from_text(text):
    if not text:
        return None

    match = re.search(r"([\d,.]+)\s*(K|M|B)?\s*[Ff]ollowers", text, re.IGNORECASE)

    if not match:
        return None

    return convert_number(match.group(1), match.group(2))
