from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencies import get_current_user, require_role

router = APIRouter()


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[schemas.UserOut])
def read_users(
    db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["admin"]))
):
    return db.query(models.User).all()


@router.put("/{user_id}/role", response_model=schemas.UserOut)
def update_user_role(
    user_id: int,
    role_update: schemas.UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"])),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user
