"""Profile read and update."""
from app.jwt_validation import validate_token

_PROFILES = {
    "u1": {"name": "Ada", "bio": "Engineer"},
    "u2": {"name": "Grace", "bio": "Admiral"},
}

MAX_BIO_LENGTH = 160


def get_profile(token: str) -> dict:
    """Return the profile of the user identified by a valid token."""
    claims = validate_token(token)
    profile = _PROFILES.get(claims["sub"])
    if profile is None:
        raise ValueError("profile not found")
    return dict(profile)


def update_bio(token: str, bio: str) -> dict:
    """Update the bio of the user identified by a valid token."""
    if len(bio) > MAX_BIO_LENGTH:
        raise ValueError("bio too long")

    claims = validate_token(token)
    profile = _PROFILES.get(claims["sub"])
    if profile is None:
        raise ValueError("profile not found")
    return {**profile, "bio": bio}