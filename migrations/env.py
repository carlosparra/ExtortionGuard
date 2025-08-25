# --- make 'app' importable when running alembic ---
from pathlib import Path
import sys
ROOT = str(Path(__file__).resolve().parents[1])  # carpeta raíz del repo
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# --------------------------------------------------

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# IMPORTA DESPUÉS DE INYECTAR sys.path
from app.db.models import Base  # noqa: E402
from app.core.config import settings  # noqa: E402

config = context.config

# Usa la DATABASE_URL de tu Settings si no hay una en alembic.ini
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Carga de logging desde alembic.ini (opcional, no fallar si faltan secciones)
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except KeyError:
        # alembic.ini sin [formatters]/[handlers]/[loggers]
        pass

# Metadata de tus modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo online."""
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
            render_as_batch=is_sqlite,  # <<<<< clave para SQLite
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
