import secrets
import uuid

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
        table_name = "user"


class Session(Model):
    session_id = UUIDField(primary_key=True, default=uuid.uuid4)
    cookie = CharField()
    user = ForeignKeyField(User)

    class Meta:
        database = db
        table_name = "session"


def seed_db() -> None:
    db.drop_tables([User, Session])
    db.create_tables([User, Session])
    User.create(username="administrator", password=secrets.token_hex(16))
    User.create(username=SQLI2_USERNAME, password=secrets.token_hex(16))
