Backend for Guilt Eater

This module defines the database schema (SQLAlchemy models) and Pydantic schemas.

Structure:

- `db/session.py` - SQLAlchemy engine and session
- `models/models.py` - ORM models: users, goals, wallet_ledger, violations, transactions
- `schemas/schemas.py` - Pydantic request/response models
- `api/router.py` - minimal API router (health)
- `auth/` - auth utilities and JWT helper (scaffold)
- `main.py` - FastAPI app and startup table creation

To run locally (use Neon/Postgres or local Postgres):

1. copy `.env.example` to `.env` inside the `backend/` folder and set `DATABASE_URL` to your Neon/Postgres URL
2. python -m venv .venv
3. source .venv/Scripts/activate # or the appropriate activate for your shell
4. pip install -r requirements.txt
5. uvicorn backend.main:app --reload

Quick install (recommended packages):

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary authlib python-jose passlib[bcrypt] httpx razorpay apscheduler python-dotenv pydantic
```

Project summary: Digital Discipline – Commitment Based Habit Control App. Backend contains schema and auth scaffolding; next steps: implement Google OAuth, JWT middleware, Razorpay flow, and violation engine.
