from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from auth.security import get_current_user
from db.session import get_db
from crud.crud import get_user_by_id

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get('/me')
def me(response: Response, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # returns the current user information; X-Access-Token header will be set by dependency
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "picture": user.picture
    }
