#!/usr/bin/env python
import subprocess
import sys
import time
from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def wait_for_db(max_retries=30):
    print("Waiting for database to be ready...")
    engine = create_engine(settings.database_url)

    for i in range(max_retries):
        try:
            conn = engine.connect()
            conn.close()
            print("Database is ready!")
            return True
        except OperationalError:
            print(f"Database not ready yet. Retry {i+1}/{max_retries}")
            time.sleep(2)

    print("Failed to connect to database")
    return False


def run_migrations():
    if not wait_for_db():
        sys.exit(1)

    print("Running migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Migrations completed successfully!")
        print(result.stdout)
    else:
        print("Alembic migration failed, creating tables directly...")
        from src.database import Base, engine
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")


if __name__ == "__main__":
    run_migrations()