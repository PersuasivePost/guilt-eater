import os
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

# Load env from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Keep only Android (mobile) flow: we only need the Google client ID to verify id_tokens
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')


def verify_google_token(token_string: str) -> dict:
    """Verify a Google id_token and return the claims."""
    try:
        # Verify the token using Google's official library
        idinfo = id_token.verify_oauth2_token(
            token_string, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        # Token is valid, return the claims
        return idinfo
    except Exception as e:
        print(f"Token verification error: {e}")
        raise ValueError(f"Invalid token: {str(e)}")
