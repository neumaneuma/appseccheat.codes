import secrets
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from peewee import CharField, ForeignKeyField, Model, PostgresqlDatabase, UUIDField

SQLI2_USERNAME = "batman"


class Database:
    _instance: PostgresqlDatabase | None = None

    @classmethod
    def get_instance(cls) -> PostgresqlDatabase:
        if cls._instance is None:
            db = PostgresqlDatabase(
                "postgres", user="postgres", password="postgres", host="db", port=5432
            )
            # reset/instantiate db
            db.drop_tables([User, Session])
            db.create_tables([User, Session])
            User.create(username="administrator", password=secrets.token_hex(16))
            User.create(username=SQLI2_USERNAME, password=secrets.token_hex(16))

        cls._instance = db
        return cls._instance


db = Database.get_instance()


class User(Model):
    user_id = UUIDField(primary_key=True, default=uuid.uuid4())
    username = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = "user"


class Session(Model):
    session_id = UUIDField(primary_key=True, default=uuid.uuid4())
    cookie = CharField()
    user = ForeignKeyField(User)

    class Meta:
        database = db
        table_name = "session"


@asynccontextmanager
async def get_db() -> AsyncGenerator[PostgresqlDatabase, None]:
    try:
        db.connect()
        yield db
    finally:
        db.close()
