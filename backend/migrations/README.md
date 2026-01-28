# Database Migrations

This folder contains database migration scripts to update the database schema.

## How to Run Migrations

### Migration: Add session_token column

**Purpose:** Adds `session_token` column to `users` table for enforcing single device login for parent accounts.

**When to run:** After pulling code changes that include the session token security feature.

**Command:**

```bash
cd backend
python migrations/add_session_token.py
```

This migration is safe to run multiple times - it will check if the column already exists before attempting to add it.

## Creating New Migrations

When you make changes to the database models in `backend/models/models.py`:

1. Create a new migration script in this folder
2. Name it descriptively (e.g., `add_new_column.py`)
3. Include checks to see if the change already exists
4. Add clear documentation in this README

## Migration History

- **add_session_token.py** - Adds session_token column for single device enforcement (January 2026)
