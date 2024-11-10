import secrets
import uuid
from typing import Any

from peewee import CharField, ForeignKeyField, Model, PostgresqlDatabase, UUIDField

from backend.constants import SQLI1_USERNAME, SQLI2_USERNAME

db = PostgresqlDatabase(
    "postgres",
    user="postgres",
    password="postgres",
    host="db",
    port=5432,
    autoconnect=False,
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


def reset_db() -> None:
    with db:
        db.drop_tables([User, Session])
        db.create_tables([User, Session])
        User.create(username=SQLI1_USERNAME, password=secrets.token_hex())
        User.create(username=SQLI2_USERNAME, password=secrets.token_hex())
