import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from auth import router as auth_router
from database import Base, engine
from routers.analytics import router as analytics_router
from routers.transactions import router as transactions_router
from routers.users import router as users_router

app = FastAPI(title="Finance Tracking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    from database import SessionLocal
    from models import User
    import auth as auth_module
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            users = [
                User(name="Admin", email="admin@example.com", hashed_password=auth_module.get_password_hash("adminpass"), role="admin"),
                User(name="Analyst", email="analyst@example.com", hashed_password=auth_module.get_password_hash("analystpass"), role="analyst"),
                User(name="Viewer", email="viewer@example.com", hashed_password=auth_module.get_password_hash("viewerpass"), role="viewer"),
            ]
            db.add_all(users)
            db.commit()
            print("✅ Seed users created!")
        else:
            print("✅ Users already exist")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Finance Tracking System is running!", "docs": "/docs"}
