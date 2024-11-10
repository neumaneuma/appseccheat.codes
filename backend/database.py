import secrets
import uuid
from typing import Any

import bcrypt
from peewee import CharField, ForeignKeyField, Model, PostgresqlDatabase, UUIDField

SQLI2_USERNAME = "batman"


db = PostgresqlDatabase(
    "postgres", user="postgres", password="postgres", host="db", port=5432
)


class User(Model):
    user_id = UUIDField(primary_key=True, default=uuid.uuid4)
    username = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = "appsec_cheat_codes_user"


class Session(Model):
    session_id = UUIDField(primary_key=True, default=uuid.uuid4)
    cookie = CharField()
    user = ForeignKeyField(User)

    class Meta:
        database = db
        table_name = "session"


def deserialize_user(result: Any | None) -> User | None:
    if result is None:
        return None
    user = User()
    user.user_id = result[0]
    user.username = result[1]
    user.password = result[2]
    return user


def deserialize_session(result: Any | None) -> Session | None:
    if result is None:
        return None
    session = Session()
    session.session_id = result[0]
    session.cookie = result[1]
    session.user = result[2]
    return session


def seed_db() -> None:
    db.drop_tables([User, Session])
    db.create_tables([User, Session])
    User.create(
        username="administrator",
        password=bcrypt.hashpw(secrets.token_hex().encode(), bcrypt.gensalt()),
    )
    User.create(
        username=SQLI2_USERNAME,
        password=bcrypt.hashpw(secrets.token_hex().encode(), bcrypt.gensalt()),
    )
