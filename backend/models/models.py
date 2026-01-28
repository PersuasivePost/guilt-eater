from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from db.session import Base
import enum


class RoleEnum(str, enum.Enum):
    parent = "parent"
    child = "child"
    individual = "individual"


class GoalStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class WalletStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    withdrawn = "withdrawn"


class TransactionType(str, enum.Enum):
    deposit = "deposit"
    penalty = "penalty"
    withdrawal = "withdrawal"


class TransactionStatus(str, enum.Enum):
    success = "success"
    failed = "failed"
    pending = "pending"


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.individual)
    parent_id = Column(String, ForeignKey("users.id"), nullable=True)
    session_token = Column(String, nullable=True)  # For single device session enforcement (parents only)
    created_at = Column(DateTime, default=datetime.utcnow)

    children = relationship("User", backref="parent", remote_side=[id])
    goals = relationship("Goal", back_populates="user")
    wallets = relationship("WalletLedger", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    linking_codes = relationship("LinkingCode", back_populates="parent", foreign_keys="LinkingCode.parent_id")


class LinkingCode(Base):
    __tablename__ = "linking_codes"
    id = Column(String, primary_key=True, default=gen_uuid)
    parent_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    code = Column(String(6), unique=True, nullable=False, index=True)
    is_used = Column(Boolean, default=False)
    used_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # Code expires after 24 hours
    used_at = Column(DateTime, nullable=True)

    parent = relationship("User", back_populates="linking_codes", foreign_keys=[parent_id])
    used_by = relationship("User", foreign_keys=[used_by_user_id])


class Goal(Base):
    __tablename__ = "goals"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    app_name = Column(String, nullable=False)
    daily_limit_minutes = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    max_warnings = Column(Integer, default=2)
    penalty_percent = Column(Float, default=10.0)
    status = Column(Enum(GoalStatus), default=GoalStatus.active)

    user = relationship("User", back_populates="goals")
    wallets = relationship("WalletLedger", back_populates="goal")
    violations = relationship("Violation", back_populates="goal")
    transactions = relationship("Transaction", back_populates="goal")


class WalletLedger(Base):
    __tablename__ = "wallet_ledger"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    goal_id = Column(String, ForeignKey("goals.id"), nullable=False, index=True)
    deposit_amount = Column(Float, nullable=False)
    current_balance = Column(Float, nullable=False)
    total_penalty = Column(Float, default=0.0)
    total_warnings = Column(Integer, default=0)
    status = Column(Enum(WalletStatus), default=WalletStatus.active)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wallets")
    goal = relationship("Goal", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")


class Violation(Base):
    __tablename__ = "violations"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    goal_id = Column(String, ForeignKey("goals.id"), nullable=False, index=True)
    app_name = Column(String, nullable=False)
    used_minutes = Column(Integer, nullable=False)
    limit_minutes = Column(Integer, nullable=False)
    warning_number = Column(Integer, nullable=False)
    penalty_applied = Column(Boolean, default=False)
    penalty_amount = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    goal = relationship("Goal", back_populates="violations")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    goal_id = Column(String, ForeignKey("goals.id"), nullable=True, index=True)
    wallet_id = Column(String, ForeignKey("wallet_ledger.id"), nullable=True, index=True)
    razorpay_payment_id = Column(String, nullable=True)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.pending)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    goal = relationship("Goal", back_populates="transactions")
    wallet = relationship("WalletLedger", back_populates="transactions")
