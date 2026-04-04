from datetime import date
from typing import Optional, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencies import get_current_user, require_role

router = APIRouter()


@router.post("/", response_model=schemas.TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"])),
):
    transaction = models.Transaction(
        amount=transaction_in.amount,
        type=transaction_in.type,
        category=transaction_in.category,
        date=transaction_in.date,
        notes=transaction_in.notes,
        user_id=current_user.id,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/", response_model=list[schemas.TransactionOut])
def list_transactions(
    transaction_type: Optional[Literal["income", "expense"]] = Query(None, alias="type"),
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    query = db.query(models.Transaction)
    if transaction_type:
        query = query.filter(models.Transaction.type == transaction_type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    transactions = query.order_by(models.Transaction.date.desc()).offset((page - 1) * limit).limit(limit).all()
    return transactions


@router.get("/{transaction_id}", response_model=schemas.TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["viewer", "analyst", "admin"])),
):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=schemas.TransactionOut)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"])),
):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    if transaction_update.amount is not None:
        transaction.amount = transaction_update.amount
    if transaction_update.type is not None:
        transaction.type = transaction_update.type
    if transaction_update.category is not None:
        transaction.category = transaction_update.category
    if transaction_update.date is not None:
        transaction.date = transaction_update.date
    if transaction_update.notes is not None:
        transaction.notes = transaction_update.notes
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"])),
):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}
