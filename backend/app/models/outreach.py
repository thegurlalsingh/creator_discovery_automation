class Outreach:
    """
    Represents outreach generated for one creator.

    Contains both:

        1. Email
        2. Instagram DM
    """

    def __init__(
        self,
        creator_id,
        email_subject=None,
        email_body=None,
        instagram_dm=None,
        email_status="pending",
        instagram_dm_status="pending",
        email_sent_at=None,
        instagram_dm_sent_at=None,
    ):

        self.creator_id = creator_id

        # Email
        self.email_subject = email_subject
        self.email_body = email_body
        self.email_status = email_status
        self.email_sent_at = email_sent_at

        # Instagram DM
        self.instagram_dm = instagram_dm
        self.instagram_dm_status = instagram_dm_status
        self.instagram_dm_sent_at = instagram_dm_sent_at

    def to_dict(self):

        return {
            "creator_id": self.creator_id,
            "email_subject": self.email_subject,
            "email_body": self.email_body,
            "email_status": self.email_status,
            "email_sent_at": self.email_sent_at,
            "instagram_dm": self.instagram_dm,
            "instagram_dm_status": self.instagram_dm_status,
            "instagram_dm_sent_at": self.instagram_dm_sent_at,
        }
