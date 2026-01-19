from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str]
    picture: Optional[str]
    role: Optional[str]
    parent_id: Optional[str]


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class GoalBase(BaseModel):
    app_name: str
    daily_limit_minutes: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    max_warnings: Optional[int] = 2
    penalty_percent: Optional[float] = 10.0
    status: Optional[str] = "active"


class GoalCreate(GoalBase):
    user_id: str


class GoalRead(GoalBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True


class WalletBase(BaseModel):
    deposit_amount: float
    current_balance: float
    total_penalty: Optional[float] = 0.0
    total_warnings: Optional[int] = 0
    status: Optional[str] = "active"


class WalletCreate(WalletBase):
    user_id: str
    goal_id: str


class WalletRead(WalletBase):
    id: str
    user_id: str
    goal_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class ViolationBase(BaseModel):
    app_name: str
    used_minutes: int
    limit_minutes: int
    warning_number: int
    penalty_applied: bool = False
    penalty_amount: float = 0.0


class ViolationCreate(ViolationBase):
    user_id: str
    goal_id: str


class ViolationRead(ViolationBase):
    id: str
    user_id: str
    goal_id: str
    timestamp: datetime

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    razorpay_payment_id: Optional[str]
    type: str
    amount: float
    status: Optional[str] = "pending"


class TransactionCreate(TransactionBase):
    user_id: str
    goal_id: Optional[str]
    wallet_id: Optional[str]


class TransactionRead(TransactionBase):
    id: str
    user_id: str
    goal_id: Optional[str]
    wallet_id: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
