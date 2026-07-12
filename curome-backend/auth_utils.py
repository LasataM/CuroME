from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

# ------------------------------------------------------------------
# JWT Configuration
# ------------------------------------------------------------------

# IMPORTANT:
# Move this to an environment variable (.env) before production.
SECRET_KEY = "your-very-secure-secret-key"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ------------------------------------------------------------------
# Create JWT
# ------------------------------------------------------------------

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
):
    """
    Creates a signed JWT access token.
    """

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + (
            expires_delta
            if expires_delta
            else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


# ------------------------------------------------------------------
# Decode JWT
# ------------------------------------------------------------------

def decode_access_token(token: str):
    """
    Validates and decodes a JWT.

    Returns the payload if valid.
    Raises JWTError if invalid or expired.
    """

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


# ------------------------------------------------------------------
# Extract User Identity
# ------------------------------------------------------------------

def get_email_from_token(token: str):
    """
    Extracts the user's email (stored as 'sub')
    from the JWT.

    Returns:
        email (str)

    Raises:
        JWTError
        ValueError
    """

    payload = decode_access_token(token)

    email = payload.get("sub")

    if email is None:
        raise ValueError("Token missing subject")

    return email