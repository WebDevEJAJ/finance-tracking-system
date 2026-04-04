from datetime import date, datetime
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Optional[str] = Field(default="viewer")

    @validator("role")
    def validate_role(cls, value: str) -> str:
        allowed = {"admin", "analyst", "viewer"}
        if value not in allowed:
            raise ValueError("role must be admin, analyst, or viewer")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserRoleUpdate(BaseModel):
    role: str

    @validator("role")
    def validate_role(cls, value: str) -> str:
        allowed = {"admin", "analyst", "viewer"}
        if value not in allowed:
            raise ValueError("role must be admin, analyst, or viewer")
        return value


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: str
    category: str = Field(..., min_length=1)
    date: date
    notes: Optional[str] = None

    @validator("type")
    def validate_type(cls, value: str) -> str:
        if value not in {"income", "expense"}:
            raise ValueError("type must be income or expense")
        return value

    @validator("date")
    def validate_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("date must not be in the future")
        return value


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

    @validator("type")
    def validate_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if value not in {"income", "expense"}:
            raise ValueError("type must be income or expense")
        return value

    @validator("date")
    def validate_date(cls, value: Optional[date]) -> Optional[date]:
        if value is None:
            return value
        if value > date.today():
            raise ValueError("date must not be in the future")
        return value


class TransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    notes: Optional[str]
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None


class SummaryOut(BaseModel):
    total_income: float
    total_expenses: float
    current_balance: float
    total_transactions: int

    class Config:
        orm_mode = True
