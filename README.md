# Finance Tracking System Backend

## Project Overview

This is a production-quality backend for a finance tracking system built with FastAPI, SQLite, SQLAlchemy, JWT authentication, and role-based access control. The backend supports user registration, login, transactions management, analytics, and strict role permissions.

## Setup Instructions

1. Create and activate a Python virtual environment:

```bash
python -m venv env
source env/Scripts/activate   # Windows PowerShell
# or
source env/bin/activate       # macOS/Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Seed the database with test users and sample transactions:

```bash
python seed.py
```

4. Run the development server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. Open Swagger UI:

`http://127.0.0.1:8000/docs`

## API Endpoints

### Auth

- `POST /auth/register` - Register a new user. No auth required.
- `POST /auth/login` - Login and receive a JWT access token.

### Transactions

- `POST /transactions/` - Create transaction. Role: admin.
- `GET /transactions/` - List transactions. Role: viewer, analyst, admin.
- `GET /transactions/{id}` - Get transaction by ID. Role: viewer, analyst, admin.
- `PUT /transactions/{id}` - Update transaction. Role: admin.
- `DELETE /transactions/{id}` - Delete transaction. Role: admin.

### Analytics

- `GET /analytics/summary` - Summary totals. Role: viewer, analyst, admin.
- `GET /analytics/by-category` - Category breakdown. Role: analyst, admin.
- `GET /analytics/monthly` - Monthly totals. Role: analyst, admin.
- `GET /analytics/recent` - Last 5 transactions. Role: viewer, analyst, admin.

### Users

- `GET /users/me` - Current user profile. Any authenticated user.
- `GET /users/` - List all users. Role: admin.
- `PUT /users/{id}/role` - Update user role. Role: admin.

## Sample curl Commands

### Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"secret123","role":"viewer"}'
```

### Login

Use the Swagger UI `Authorize` button with username and password, or call login with form data:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=adminpass"
```

### Create Transaction (Admin)

```bash
curl -X POST http://127.0.0.1:8000/transactions/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 250.5, "type": "expense", "category": "office", "date": "2024-04-01", "notes": "Office supplies"}'
```

### Get Transactions

```bash
curl -X GET "http://127.0.0.1:8000/transactions/?page=1&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

### Get Summary Analytics

```bash
curl -X GET http://127.0.0.1:8000/analytics/summary \
  -H "Authorization: Bearer <TOKEN>"
```

### Get Category Analytics

```bash
curl -X GET http://127.0.0.1:8000/analytics/by-category \
  -H "Authorization: Bearer <TOKEN>"
```

### Get Current User

```bash
curl -X GET http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <TOKEN>"
```

### Update User Role (Admin)

```bash
curl -X PUT http://127.0.0.1:8000/users/2/role \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"role":"analyst"}'
```

## Login Credentials for Test Users

- Admin: `admin@example.com` / `adminpass`
- Analyst: `analyst@example.com` / `analystpass`
- Viewer: `viewer@example.com` / `viewerpass`

## Assumptions Made

- The app uses a local SQLite database file named `finance.db` in the project root.
- Transactions are created on behalf of the authenticated admin user who creates them.
- Role enforcement is strict and returns `403 Forbidden` for unauthorized actions.
- Input validation is handled with Pydantic and returns JSON error details.
- The JWT secret is hard-coded for local testing and should be replaced in production.
