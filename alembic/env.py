from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importa il tuo modello e la Base da app.py
from app import Base, DBUser  # Modifica 'app' con il nome del tuo file se diverso

# Configurazione di Alembic
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata  # Collegamento ai metadati di SQLAlchemy

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()