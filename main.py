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

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
app.include_router(users_router, prefix="/users", tags=["users"])


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
