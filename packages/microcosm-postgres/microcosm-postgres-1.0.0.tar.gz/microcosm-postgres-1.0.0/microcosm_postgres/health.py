"""
Simple Postgres health check.

"""
from microcosm_postgres.context import SessionContext


def check_health(graph):
    """
    Basic database health check.

    """
    SessionContext.session.execute("SELECT 1;")


def check_alembic(graph):
    """
    Check connectivity to an alembic database.

    Returns the current migration.

    """
    return SessionContext.session.execute(
        "SELECT version_num FROM alembic_version LIMIT 1;",
    ).scalar()
