from datetime import date

import models
from auth import get_password_hash
from database import Base, SessionLocal, engine


def seed_data() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_users = db.query(models.User).count()
        if existing_users > 0:
            print("Seed data already exists. Skipping insert.")
            print("Admin: admin@example.com / adminpass")
            print("Analyst: analyst@example.com / analystpass")
            print("Viewer: viewer@example.com / viewerpass")
            return

        admin = models.User(
            name="Admin User",
            email="admin@example.com",
            hashed_password=get_password_hash("adminpass"),
            role="admin",
        )
        analyst = models.User(
            name="Analyst User",
            email="analyst@example.com",
            hashed_password=get_password_hash("analystpass"),
            role="analyst",
        )
        viewer = models.User(
            name="Viewer User",
            email="viewer@example.com",
            hashed_password=get_password_hash("viewerpass"),
            role="viewer",
        )
        db.add_all([admin, analyst, viewer])
        db.commit()
        db.refresh(admin)
        db.refresh(analyst)
        db.refresh(viewer)

        sample_transactions = [
            {"amount": 1200.0, "type": "income", "category": "salary", "date": date(2024, 1, 3), "notes": "Monthly salary", "user_id": admin.id},
            {"amount": 450.0, "type": "expense", "category": "groceries", "date": date(2024, 1, 5), "notes": "Grocery shopping", "user_id": admin.id},
            {"amount": 60.0, "type": "expense", "category": "transport", "date": date(2024, 1, 8), "notes": "Train pass", "user_id": analyst.id},
            {"amount": 250.0, "type": "income", "category": "freelance", "date": date(2024, 1, 10), "notes": "Freelance milestone", "user_id": analyst.id},
            {"amount": 120.0, "type": "expense", "category": "utilities", "date": date(2024, 1, 12), "notes": "Electricity bill", "user_id": viewer.id},
            {"amount": 95.0, "type": "expense", "category": "food", "date": date(2024, 1, 15), "notes": "Dinner out", "user_id": admin.id},
            {"amount": 1800.0, "type": "income", "category": "salary", "date": date(2024, 2, 1), "notes": "February salary", "user_id": admin.id},
            {"amount": 520.0, "type": "expense", "category": "rent", "date": date(2024, 2, 3), "notes": "Monthly rent", "user_id": admin.id},
            {"amount": 130.0, "type": "expense", "category": "groceries", "date": date(2024, 2, 6), "notes": "Weekly groceries", "user_id": analyst.id},
            {"amount": 340.0, "type": "income", "category": "bonus", "date": date(2024, 2, 14), "notes": "Performance bonus", "user_id": analyst.id},
            {"amount": 55.0, "type": "expense", "category": "transport", "date": date(2024, 2, 18), "notes": "Bus pass", "user_id": viewer.id},
            {"amount": 400.0, "type": "expense", "category": "health", "date": date(2024, 2, 20), "notes": "Doctor appointment", "user_id": admin.id},
            {"amount": 2000.0, "type": "income", "category": "salary", "date": date(2024, 3, 1), "notes": "March salary", "user_id": admin.id},
            {"amount": 610.0, "type": "expense", "category": "rent", "date": date(2024, 3, 2), "notes": "March rent", "user_id": admin.id},
            {"amount": 75.0, "type": "expense", "category": "food", "date": date(2024, 3, 4), "notes": "Lunch meeting", "user_id": analyst.id},
            {"amount": 95.0, "type": "expense", "category": "utilities", "date": date(2024, 3, 9), "notes": "Water bill", "user_id": viewer.id},
            {"amount": 360.0, "type": "income", "category": "freelance", "date": date(2024, 3, 12), "notes": "Client project", "user_id": analyst.id},
            {"amount": 220.0, "type": "expense", "category": "groceries", "date": date(2024, 3, 15), "notes": "Market run", "user_id": admin.id},
            {"amount": 150.0, "type": "expense", "category": "entertainment", "date": date(2024, 3, 18), "notes": "Concert ticket", "user_id": viewer.id},
            {"amount": 89.0, "type": "expense", "category": "subscriptions", "date": date(2024, 3, 22), "notes": "Streaming service", "user_id": analyst.id},
        ]

        for transaction_data in sample_transactions:
            transaction = models.Transaction(**transaction_data)
            db.add(transaction)
        db.commit()

        print("Seed completed successfully.")
        print("Login credentials:")
        print("- Admin: admin@example.com / adminpass")
        print("- Analyst: analyst@example.com / analystpass")
        print("- Viewer: viewer@example.com / viewerpass")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
