from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from models.models import User, LinkingCode
from auth.security import get_current_user
from datetime import datetime, timedelta
import random
import string

router = APIRouter()


def generate_unique_code(db: Session) -> str:
    """Generate a unique 6-digit linking code"""
    while True:
        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Check if code already exists and is not expired
        existing = db.query(LinkingCode).filter(
            LinkingCode.code == code,
            LinkingCode.expires_at > datetime.utcnow()
        ).first()
        
        if not existing:
            return code


@router.post('/generate-linking-code')
async def generate_linking_code(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a linking code for parent to share with child"""
    
    # Only parents can generate linking codes
    if current_user.role != 'parent':
        raise HTTPException(status_code=403, detail='Only parents can generate linking codes')
    
    # Check if there's an existing unused code
    existing_code = db.query(LinkingCode).filter(
        LinkingCode.parent_id == current_user.id,
        LinkingCode.is_used == False,
        LinkingCode.expires_at > datetime.utcnow()
    ).first()
    
    if existing_code:
        # Return existing valid code
        return {
            'code': existing_code.code,
            'parent_id': current_user.id,
            'parent_name': current_user.name,
            'expires_at': existing_code.expires_at.isoformat(),
            'qr_data': f"{current_user.id}:{existing_code.code}"
        }
    
    # Generate new code
    code = generate_unique_code(db)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    linking_code = LinkingCode(
        parent_id=current_user.id,
        code=code,
        expires_at=expires_at
    )
    
    db.add(linking_code)
    db.commit()
    db.refresh(linking_code)
    
    return {
        'code': code,
        'parent_id': current_user.id,
        'parent_name': current_user.name,
        'expires_at': expires_at.isoformat(),
        'qr_data': f"{current_user.id}:{code}"
    }


@router.post('/verify-linking-code')
async def verify_linking_code(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify linking code and link child to parent
    payload: {"code": "123456"} or {"qr_data": "parent_id:code"}
    """
    
    # Only children or users without parent can use linking codes
    if current_user.role == 'parent':
        raise HTTPException(status_code=403, detail='Parents cannot use linking codes')
    
    if current_user.parent_id:
        raise HTTPException(status_code=400, detail='Already linked to a parent')
    
    # Extract code
    code = payload.get('code')
    qr_data = payload.get('qr_data')
    
    if qr_data:
        # Parse QR data: "parent_id:code"
        try:
            parts = qr_data.split(':')
            if len(parts) != 2:
                raise ValueError('Invalid QR data format')
            parent_id, code = parts
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid QR code format')
    elif not code:
        raise HTTPException(status_code=400, detail='Code or QR data required')
    
    # Find the linking code
    linking_code = db.query(LinkingCode).filter(
        LinkingCode.code == code,
        LinkingCode.is_used == False,
        LinkingCode.expires_at > datetime.utcnow()
    ).first()
    
    if not linking_code:
        raise HTTPException(status_code=404, detail='Invalid or expired linking code')
    
    # Get parent
    parent = db.query(User).filter(User.id == linking_code.parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail='Parent not found')
    
    # Link child to parent
    current_user.parent_id = parent.id
    current_user.role = 'child'  # Ensure role is set to child
    
    # Mark code as used
    linking_code.is_used = True
    linking_code.used_by_user_id = current_user.id
    linking_code.used_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return {
        'success': True,
        'parent_name': parent.name,
        'parent_email': parent.email,
        'child_name': current_user.name,
        'child_email': current_user.email,
        'linked_at': datetime.utcnow().isoformat()
    }


@router.get('/my-children')
async def get_my_children(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of children linked to current parent"""
    
    if current_user.role != 'parent':
        raise HTTPException(status_code=403, detail='Only parents can view children')
    
    children = db.query(User).filter(User.parent_id == current_user.id).all()
    
    return {
        'children': [
            {
                'id': child.id,
                'name': child.name,
                'email': child.email,
                'created_at': child.created_at.isoformat()
            }
            for child in children
        ]
    }


@router.get('/my-parent')
async def get_my_parent(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get parent info for current child"""
    
    if current_user.role != 'child':
        raise HTTPException(status_code=403, detail='Only children can view parent')
    
    if not current_user.parent_id:
        raise HTTPException(status_code=404, detail='No parent linked')
    
    parent = db.query(User).filter(User.id == current_user.parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail='Parent not found')
    
    return {
        'id': parent.id,
        'name': parent.name,
        'email': parent.email
    }
