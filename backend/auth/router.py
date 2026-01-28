from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from auth import security
from db.session import get_db
from sqlalchemy.orm import Session
from models.models import User
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import os

router = APIRouter()

# Get Google Client ID from environment
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')


@router.post('/token')
async def token_exchange(payload: dict, db: Session = Depends(get_db)):
    """Accepts a Google id_token (from Android mobile) and returns our JWT.
    payload: {"id_token": "...", "role": "individual|parent|child"}
    """
    token_string = payload.get('id_token')
    if not token_string:
        raise HTTPException(status_code=400, detail='id_token required')
    
    # Get role from payload, default to 'individual' if not provided
    user_role = payload.get('role', 'individual')
    if user_role not in ['individual', 'parent', 'child']:
        raise HTTPException(status_code=400, detail='invalid role. Must be individual, parent, or child')

    # Verify id_token using Google's official library
    try:
        print(f"Attempting to verify id_token with CLIENT_ID: {GOOGLE_CLIENT_ID}")
        # Verify the token
        claims = id_token.verify_oauth2_token(
            token_string, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        print(f"Token verified successfully! Claims: {claims}")
    except ValueError as e:
        print(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f'invalid id_token: {str(e)}')
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=400, detail=f'token verification error: {str(e)}')

    email = claims.get('email')
    if not email:
        raise HTTPException(status_code=400, detail='email not present in token')

    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"Creating new user: {email} with role: {user_role}")
        user = User(
            email=email, 
            name=claims.get('name'), 
            picture=claims.get('picture'),
            role=user_role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        print(f"User already exists: {email} with role: {user.role}")

    token = security.create_access_token(user.id)
    print(f"Successfully created JWT for user {user.id}")
    return JSONResponse({'access_token': token, 'token_type': 'bearer'})
