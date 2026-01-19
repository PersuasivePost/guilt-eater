from sqlalchemy.orm import Session
from models.models import User, Goal, WalletLedger, Violation, Transaction


def create_user(db: Session, **kwargs) -> User:
    user = User(**kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_goal(db: Session, **kwargs) -> Goal:
    goal = Goal(**kwargs)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def create_wallet(db: Session, **kwargs) -> WalletLedger:
    wallet = WalletLedger(**kwargs)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet
