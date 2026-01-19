from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from ..auth.oauth import oauth, get_google_user
from ..auth import security
from ..db.session import get_db
from sqlalchemy.orm import Session
from ..models.models import User
import os

router = APIRouter()


@router.get('/google/login')
async def login(request: Request):
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/google/callback')
async def callback(request: Request, db: Session = Depends(get_db)):
    userinfo = await get_google_user(request)
    if not userinfo:
        raise HTTPException(status_code=400, detail='Google auth failed')

    # find or create user
    email = userinfo.get('email')
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=userinfo.get('name'), picture=userinfo.get('picture'))
        db.add(user)
        db.commit()
        db.refresh(user)

    token = security.create_access_token(user.id)
    # For web flow redirect to frontend with token (adjust frontend URL in env later)
    frontend_redirect = os.getenv('FRONTEND_REDIRECT', 'http://localhost:3000')
    return RedirectResponse(f"{frontend_redirect}/auth?token={token}")


@router.post('/token')
async def token_exchange(payload: dict, db: Session = Depends(get_db)):
    """Accepts a Google id_token (from mobile) and returns our JWT.
    payload: {"id_token": "..."}
    """
    id_token = payload.get('id_token')
    if not id_token:
        raise HTTPException(status_code=400, detail='id_token required')

    # Verify id_token via authlib / google
    try:
        # Use oauth client to parse id_token
        claims = await oauth.google.parse_id_token(None, {'id_token': id_token, 'access_token': None})
    except Exception:
        # fallback - let authlib handle errors upstream
        raise HTTPException(status_code=400, detail='invalid id_token')

    email = claims.get('email')
    if not email:
        raise HTTPException(status_code=400, detail='email not present in token')

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=claims.get('name'), picture=claims.get('picture'))
        db.add(user)
        db.commit()
        db.refresh(user)

    token = security.create_access_token(user.id)
    return JSONResponse({'access_token': token, 'token_type': 'bearer'})
