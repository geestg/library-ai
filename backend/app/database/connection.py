import os

from urllib.parse import quote_plus

from sqlalchemy import (
    create_engine,
)

from sqlalchemy.orm import (
    sessionmaker,
)

from app.database.base import (
    Base,
)


# =====================================
# DATABASE CONFIGURATION
# =====================================

def build_database_url() -> str:

    # =================================
    # EXPLICIT DATABASE URL
    # =================================

    explicit_database_url = (

        os.getenv(
            "DATABASE_URL",
            "",
        ).strip()

    )

    if explicit_database_url:

        return explicit_database_url

    # =================================
    # POSTGRES COMPONENTS
    # =================================

    postgres_user = (

        os.getenv(
            "POSTGRES_USER",
            "",
        ).strip()

    )

    postgres_password = (

        os.getenv(
            "POSTGRES_PASSWORD",
            "",
        )

    )

    postgres_database = (

        os.getenv(
            "POSTGRES_DB",
            "",
        ).strip()

    )

    postgres_host = (

        os.getenv(
            "POSTGRES_HOST",
            "postgres",
        ).strip()

        or "postgres"

    )

    postgres_port = (

        os.getenv(
            "POSTGRES_PORT",
            "5432",
        ).strip()

        or "5432"

    )

    # =================================
    # VALIDATE REQUIRED CONFIG
    # =================================

    missing_variables = [

        variable_name

        for (

            variable_name,

            variable_value,

        ) in [

            (
                "POSTGRES_USER",
                postgres_user,
            ),

            (
                "POSTGRES_PASSWORD",
                postgres_password,
            ),

            (
                "POSTGRES_DB",
                postgres_database,
            ),

        ]

        if not variable_value

    ]

    if missing_variables:

        raise RuntimeError(

            (
                "Missing PostgreSQL "
                "configuration: "
                + ", ".join(
                    missing_variables
                )
            )

        )

    # =================================
    # ESCAPE CREDENTIALS
    # =================================

    encoded_user = quote_plus(
        postgres_user
    )

    encoded_password = quote_plus(
        postgres_password
    )

    encoded_database = quote_plus(
        postgres_database
    )

    # =================================
    # BUILD URL
    # =================================

    return (

        "postgresql+psycopg2://"

        f"{encoded_user}:"

        f"{encoded_password}@"

        f"{postgres_host}:"

        f"{postgres_port}/"

        f"{encoded_database}"

    )


# =====================================
# DATABASE URL
# =====================================

DATABASE_URL = (
    build_database_url()
)


# =====================================
# DATABASE ENGINE
# =====================================

database_engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    future=True,

)


# =====================================
# DATABASE SESSION FACTORY
# =====================================

database_session_factory = sessionmaker(

    bind=database_engine,

    autoflush=False,

    expire_on_commit=False,

)


# =====================================
# INITIALIZE DATABASE
# =====================================

def initialize_database():

    # =================================
    # IMPORT ORM MODELS
    # =================================

    # Import is intentionally local.
    # It registers ORM tables in
    # Base.metadata before create_all().

    from app.persistence.session import (  # noqa: F401
        WorkspaceSessionRecord,
    )

    # =================================
    # CREATE TABLES
    # =================================

    Base.metadata.create_all(

        bind=database_engine

    )