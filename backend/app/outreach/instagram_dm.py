def prepare_instagram_dm(instagram_dm):
    """
    Prepare an Instagram DM for sending.

    Currently this only returns the generated message.

    Actual Instagram sending can be implemented later
    using an appropriate Instagram API / integration.
    """

    if not instagram_dm:
        raise ValueError("Instagram DM is empty")

    return {"message": instagram_dm, "status": "pending"}
