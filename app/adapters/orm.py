from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship, registry
from sqlalchemy.sql.sqltypes import Boolean

from app.domain import model


metadata = MetaData()
mapper_registry = registry()

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("password", String(255)),
    Column("email", Integer, nullable=False),
)

git_repos = Table(
    "git_repos",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("url", String(255)),
    Column("user_id", Integer, nullable=False),
)

feedbacks = Table(
    "feedbacks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("message", String(255)),
    Column("private", Boolean, nullable=False),
    Column("giver_id", Integer, nullable=False),
    Column("git_repo_id", ForeignKey("git_repos.id")),
)


def start_mappers():
    users_mapper = mapper_registry.map_imperatively(model.User, users)
    feedbacks_mapper = mapper_registry.map_imperatively(model.Feedback, feedbacks)
    mapper_registry.map_imperatively(
        model.GitRepo,
        git_repos,
        properties={
            "_feedbacks": relationship(
                feedbacks_mapper,
                collection_class=list,
            )
        },
    )
