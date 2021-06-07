import os
import logging
import psycopg2

from sqlalchemy import text
from sqlalchemy.schema import CreateSchema

from dispatch.search.fulltext import (
    CreateSearchFunctionSQL,
    CreateSearchTriggerSQL,
)
from sqlalchemy_utils import create_database, database_exists

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from dispatch import config
from dispatch.project.models import ProjectCreate
from dispatch.organization.models import Organization
from dispatch.project import service as project_service

from .core import (
    Base,
    engine,
)


from .enums import DISPATCH_ORGANIZATION_SCHEMA_PREFIX


log = logging.getLogger(__file__)


def version_schema(script_location: str):
    """Applies alembic versioning to schema."""
    alembic_cfg = AlembicConfig(config.ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_command.stamp(alembic_cfg, "head")


def get_core_tables():
    """Fetches tables are belong to the 'dispatch' schema."""
    core_tables = []
    for _, table in Base.metadata.tables.items():
        if table.schema == "dispatch":
            core_tables.append(table)
    return core_tables


def get_tenant_tables():
    """Fetches tables that belong to their own tenant tables."""
    tenant_tables = []
    for _, table in Base.metadata.tables.items():
        if not table.schema:
            tenant_tables.append(table)
    return tenant_tables


def init_database(*, db_session):
    """Initializes a the database."""
    if not database_exists(str(config.SQLALCHEMY_DATABASE_URI)):
        create_database(str(config.SQLALCHEMY_DATABASE_URI))

    schema_name = "dispatch"
    if not engine.dialect.has_schema(engine, schema_name):
        engine.execute(CreateSchema(schema_name))

    tables = get_core_tables()
    Base.metadata.create_all(engine, tables=tables)

    version_schema(script_location=config.ALEMBIC_CORE_REVISION_PATH)

    sync_triggers(tables)

    # default organization
    organization = Organization(
        name="default",
        default=True,
        description="Default dispatch organization.",
    )

    db_session.add(organization)
    db_session.commit()

    init_schema(db_session=db_session, organization=organization)


def init_schema(*, db_session, organization: Organization):
    """Initializing a new schema."""

    schema_name = f"{DISPATCH_ORGANIZATION_SCHEMA_PREFIX}_{organization.name}"
    if not engine.dialect.has_schema(engine, schema_name):
        engine.execute(CreateSchema(schema_name))

    # set the schema for table creation
    tables = get_tenant_tables()
    for t in tables:
        t.schema = schema_name

    Base.metadata.create_all(engine, tables=tables)

    # put schema under version control
    version_schema(script_location=config.ALEMBIC_TENANT_REVISION_PATH)

    sync_triggers(tables)

    # create any required default values in schema here
    #
    #
    project_service.get_or_create(
        db_session=db_session,
        project_in=ProjectCreate(
            name="default",
            default=True,
            description="Default dispatch project.",
            organization=organization,
        ),
    )


def sync_triggers(tables):
    """Syncs any required table triggers."""
    for table in tables:
        for column in table.columns:
            if column.name.endswith("search_vector"):
                if hasattr(column.type, "columns"):
                    params = dict(
                        tsvector_column=getattr(table.c, "search_vector"),
                        indexed_columns=column.type.columns,
                        options=None,
                        conn=engine,
                    )
                    classes = [
                        CreateSearchFunctionSQL,
                        CreateSearchTriggerSQL,
                    ]
                    for class_ in classes:
                        sql = class_(**params)
                        try:
                            engine.execute(str(sql), **sql.params)
                        except psycopg2.errors.DuplicateFunction:
                            pass

                    update_sql = table.update().values(
                        {column.type.columns[0]: text(column.type.columns[0])}
                    )
                    engine.execute(update_sql)
                else:
                    log.warning(
                        f"Column search_vector defined but no index columns found. Table: {table.name}"
                    )