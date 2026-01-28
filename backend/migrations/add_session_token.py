"""
Migration script to add session_token column to users table.
Run this to update your database after pulling the latest code changes.
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables")
    exit(1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='session_token'
        """))
        
        if result.fetchone():
            print("✓ session_token column already exists in users table")
        else:
            # Add session_token column
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN session_token VARCHAR
            """))
            conn.commit()
            print("✓ Successfully added session_token column to users table")
        
        print("\nMigration completed successfully!")
        
except Exception as e:
    print(f"ERROR during migration: {e}")
    exit(1)
