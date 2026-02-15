"""
Database Migration Runner
Audrey Evans Official / GlowStarLabs

Runs SQL migrations in order on startup.
"""
import os
from pathlib import Path


MIGRATIONS_DIR = Path(__file__).parent


async def run_all_migrations(pool):
    """Run all SQL migration files in order."""
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    async with pool.acquire() as conn:
        # Create migrations tracking table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)

        for migration_file in migration_files:
            filename = migration_file.name

            # Check if already applied
            row = await conn.fetchrow(
                "SELECT id FROM _migrations WHERE filename = $1",
                filename,
            )
            if row:
                continue

            # Apply migration
            sql = migration_file.read_text()
            try:
                await conn.execute(sql)
                await conn.execute(
                    "INSERT INTO _migrations (filename) VALUES ($1)",
                    filename,
                )
                print(f"  Applied migration: {filename}")
            except Exception as e:
                print(f"  Migration {filename} failed: {e}")
                # Don't fail on already-exists errors
                if "already exists" not in str(e):
                    raise
