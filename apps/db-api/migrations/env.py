from typing import TYPE_CHECKING

from alembic import context
from alembic.autogenerate import rewriter
from sqlalchemy import engine_from_config, pool

from app.config import SQLALCHEMY_DATABASE_URI_SYNC
from app.models import Base

if TYPE_CHECKING:
    from advanced_alchemy.alembic.commands import AlembicCommandConfig

__all__ = ('do_run_migrations', 'run_migrations_offline', 'run_migrations_online')


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config: 'AlembicCommandConfig' = context.config
config.set_main_option(
    'sqlalchemy.url', SQLALCHEMY_DATABASE_URI_SYNC.render_as_string(hide_password=False)
)
target_metadata = Base.metadata

writer = rewriter.Rewriter()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.

    Raises:
        RuntimeError: If the engine cannot be created from the config.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
