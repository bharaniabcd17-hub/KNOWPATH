"""Alembic environment configuration with async SQLAlchemy support."""
from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ---------------------------------------------------------------------------
# Alembic Config object (gives access to alembic.ini values)
# ---------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Import all models so autogenerate can detect schema changes.
# app.models re-exports Base and all ORM classes.
# ---------------------------------------------------------------------------
try:
    from app.database import Base  # noqa: F401

    # Import all domain models to register them with Base.metadata
    # Add imports here as domains are created:
    # from app.domains.auth import models  # noqa: F401
    # from app.domains.users import models  # noqa: F401

    target_metadata = Base.metadata
except ImportError:
    # Graceful fallback during initial scaffold (before models exist)
    target_metadata = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Override sqlalchemy.url from environment variable
# ---------------------------------------------------------------------------
database_url = os.environ.get("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
# asyncpg driver for async usage; alembic needs sync URL for migrations
# convert postgresql+asyncpg:// -> postgresql+psycopg2:// for alembic sync runner
sync_url = database_url
if database_url and "+asyncpg" in database_url:
    sync_url = database_url.replace("+asyncpg", "+psycopg2", 1)

config.set_main_option("sqlalchemy.url", sync_url or "")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DB connection required)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using an async engine (psycopg2 sync fallback for alembic)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
