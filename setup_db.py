"""
PostgreSQL + PostGIS Database Setup Script.
Run once to create the database and user.

Prerequisites:
  - PostgreSQL 16+ installed with PostGIS extension
  - psql CLI available

Usage:
  python setup_db.py

Or manually:
  psql -U postgres -c "CREATE USER geoint WITH PASSWORD 'geoint';"
  psql -U postgres -c "CREATE DATABASE geointdb OWNER geoint;"
  psql -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS postgis;"
  psql -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
  psql -U postgres -d geointdb -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
"""
import subprocess
import sys


def run_psql(command: str, db: str = "postgres"):
    """Run a psql command."""
    try:
        result = subprocess.run(
            ["psql", "-U", "postgres", "-d", db, "-c", command],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            print(f"  ✓ {command[:60]}...")
        else:
            print(f"  ⚠ {result.stderr.strip()}")
        return result.returncode == 0
    except FileNotFoundError:
        print("  ✗ psql not found. Please install PostgreSQL.")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    print("=== GEOINT Database Setup ===\n")

    print("1. Creating user 'geoint'...")
    run_psql("CREATE USER geoint WITH PASSWORD 'geoint' CREATEDB;")

    print("2. Creating database 'geointdb'...")
    run_psql("CREATE DATABASE geointdb OWNER geoint;")

    print("3. Installing PostGIS extension...")
    run_psql("CREATE EXTENSION IF NOT EXISTS postgis;", db="geointdb")

    print("4. Installing pg_trgm extension...")
    run_psql("CREATE EXTENSION IF NOT EXISTS pg_trgm;", db="geointdb")

    print("5. Installing uuid-ossp extension...")
    run_psql('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";', db="geointdb")

    print("\n6. Creating tables via SQLAlchemy...")
    try:
        from db.engine import init_db
        init_db()
        print("  ✓ All tables created successfully!")
    except Exception as e:
        print(f"  ✗ Table creation failed: {e}")
        print("    Check that PostgreSQL is running and the connection string is correct.")

    print("\n7. Seeding data...")
    try:
        from seed_data import main as seed_main
        seed_main()
        print("  ✓ Seed data loaded!")
    except Exception as e:
        print(f"  ✗ Seeding failed: {e}")

    print("\n=== Setup Complete ===")
    print("\nTo start the platform:")
    print("  python app.py        # Web server on http://localhost:8000")
    print("  python worker.py     # Background worker")


if __name__ == "__main__":
    main()
