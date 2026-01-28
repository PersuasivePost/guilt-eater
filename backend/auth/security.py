import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError

# Config via env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

JWT_SECRET = os.getenv('JWT_SECRET', 'change-me')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
# Idle timeout in seconds; default 2 days
JWT_IDLE_SECONDS = int(os.getenv('JWT_IDLE_SECONDS', str(2 * 24 * 3600)))


def hash_password_sha256(password: str, salt: Optional[str] = None) -> str:
    """Return salt$sha256hex for storage. If salt not provided a random 16-byte hex salt is generated."""
    if salt is None:
        salt = os.urandom(16).hex()
    h = hashlib.sha256()
    h.update((salt + password).encode('utf-8'))
    return f"{salt}${h.hexdigest()}"


def verify_password_sha256(stored: str, provided_password: str) -> bool:
    try:
        salt, digest = stored.split('$', 1)
    except ValueError:
        return False
    h = hashlib.sha256()
    h.update((salt + provided_password).encode('utf-8'))
    return h.hexdigest() == digest


def create_access_token(subject: str, idle_seconds: Optional[int] = None) -> str:
    """Create JWT with expiry set to now + idle_seconds (sliding inactivity window).

    The client should include the token on each request; the server can refresh the token
    and return a new one when activity occurs (sliding window).
    """
    now = datetime.utcnow()
    if idle_seconds is None:
        idle_seconds = JWT_IDLE_SECONDS
    expires = now + timedelta(seconds=idle_seconds)
    payload = {"sub": subject, "exp": int(expires.timestamp()), "iat": int(now.timestamp())}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


# FastAPI helper dependency to verify token and refresh it on activity
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Response
from sqlalchemy.orm import Session
from db.session import get_db
from models.models import User

http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    response: Response, 
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to extract user from Bearer token, verify it, and refresh token expiry.

    Sets header 'X-Access-Token' with a refreshed token. If token is missing/invalid raises 401.
    Returns the User object from database.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get('sub')
    
    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # create a new token with fresh idle window
    new_token = create_access_token(user_id)
    # set new token in response header so client can update
    response.headers['X-Access-Token'] = new_token
    return user
