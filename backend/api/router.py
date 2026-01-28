from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from auth.security import get_current_user
from db.session import get_db
from models.models import User

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get('/me')
def me(response: Response, current_user: User = Depends(get_current_user)):
    # returns the current user information; X-Access-Token header will be set by dependency
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "picture": current_user.picture,
        "role": current_user.role.value if current_user.role else None
    }
