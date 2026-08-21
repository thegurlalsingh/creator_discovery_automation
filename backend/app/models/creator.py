from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Creator:
    username: str
    name: str
    contact_email: str
    follower_count: int
    profile_url: str
    verified: bool
    bio: str
    engagement_rate: Optional[float]
    category: Optional[str]
    content_themes: List[str]

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "contact_email": self.contact_email,
            "follower_count": self.follower_count,
            "profile_url": self.profile_url,
            "verified": self.verified,
            "bio": self.bio,
            "engagement_rate": self.engagement_rate,
            "category": self.category,
            "content_themes": self.content_themes,
        }
