from contextlib import asynccontextmanager
from typing import AsyncGenerator

from peewee import CharField, Model, PostgresqlDatabase


class Database:
    _instance: PostgresqlDatabase | None = None

    @classmethod
    def get_instance(cls) -> PostgresqlDatabase:
        if cls._instance is None:
            db = PostgresqlDatabase("postgres", user="postgres", password="postgres", host="db", port=5432)
            # reset/instantiate db
            db.drop_tables([Sqli1User, Sqli2User])
            db.create_tables([Sqli1User, Sqli2User])
            Sqli1User.create(username="administrator", password="password123")

        cls._instance = db
        return cls._instance


db = Database.get_instance()


class Sqli1User(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db


class Sqli2User(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db


@asynccontextmanager
async def get_db() -> AsyncGenerator[PostgresqlDatabase, None]:
    try:
        await db.connect()
        yield db
    finally:
        await db.close()
