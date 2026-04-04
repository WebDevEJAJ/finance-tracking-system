from collections import defaultdict
from datetime import date
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencies import get_current_user, require_role

router = APIRouter()


@router.get("/summary", response_model=schemas.SummaryOut)
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    transactions = db.query(models.Transaction).all()
    total_income = sum(txn.amount for txn in transactions if txn.type == "income")
    total_expenses = sum(txn.amount for txn in transactions if txn.type == "expense")
    return schemas.SummaryOut(
        total_income=total_income,
        total_expenses=total_expenses,
        current_balance=total_income - total_expenses,
        total_transactions=len(transactions),
    )


@router.get("/by-category", response_model=Dict[str, Dict[str, float]])
def get_by_category(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "analyst"])),
):
    transactions = db.query(models.Transaction).all()
    breakdown: Dict[str, Dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for txn in transactions:
        breakdown[txn.category][txn.type] += txn.amount
    return {category: values for category, values in breakdown.items()}


@router.get("/monthly", response_model=Dict[str, Dict[str, float]])
def get_monthly_totals(
    year: Optional[int] = Query(None, ge=1900, le=2100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "analyst"])),
):
    query = db.query(models.Transaction)
    if year is not None:
        query = query.filter(models.Transaction.date >= date(year, 1, 1))
        query = query.filter(models.Transaction.date <= date(year, 12, 31))
    transactions = query.all()
    monthly: Dict[str, Dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for txn in transactions:
        key = f"{txn.date.year:04d}-{txn.date.month:02d}"
        monthly[key][txn.type] += txn.amount
    return {month: values for month, values in sorted(monthly.items())}


@router.get("/recent", response_model=List[schemas.TransactionOut])
def get_recent_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    transactions = (
        db.query(models.Transaction)
        .order_by(models.Transaction.date.desc(), models.Transaction.created_at.desc())
        .limit(5)
        .all()
    )
    return transactions
