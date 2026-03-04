# --- make 'app' importable when running alembic ---
from pathlib import Path
import sys
ROOT = str(Path(__file__).resolve().parents[1])  # repository root folder
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# --------------------------------------------------

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# IMPORT AFTER INJECTING sys.path
from app.db.models import Base  # noqa: E402
from app.core.config import settings  # noqa: E402

config = context.config

# Use DATABASE_URL from your Settings if there isn't one in alembic.ini
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Load logging from alembic.ini (optional, don't fail if sections are missing)
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except KeyError:
        # alembic.ini without [formatters]/[handlers]/[loggers]
        pass

# Your models metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        url = config.get_main_option("sqlalchemy.url")
        is_sqlite = url.startswith("sqlite")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=is_sqlite,  # <<<<< key for SQLite
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
