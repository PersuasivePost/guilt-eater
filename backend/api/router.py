from fastapi import APIRouter, Depends, Response
from auth.security import get_current_user

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get('/me')
def me(response: Response, user_id: str = Depends(get_current_user)):
    # returns the current user id; X-Access-Token header will be set by dependency
    return {"user_id": user_id}
