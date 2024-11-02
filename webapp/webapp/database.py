from pathlib import Path

from flask import Blueprint, g
from sqlalchemy import create_engine

bp = Blueprint("db", __name__)


def get_connection():
    def create_connection(password):
        engine = create_engine(
            f"{database_type}+{connector}://{user}:{password}@{host}:{port}/{database_name}",
            echo=True,
        )
        return engine.connect()

    if "connection" not in g:
        db_password = "/run/secrets/db-password"
        database_type = "mysql"
        connector = "mysqlconnector"
        user = "root"
        host = "db"
        port = "3306"
        database_name = "appsecdb"

        # Hardcode password of database to string test if docker secret file is not found
        # In truth, this is a very bad pattern, but it makes it easier for people to run the web server locally
        # The database also doesn't store any sensitive information, so I judged it to be a trade off worth taking
        if not Path(db_password).is_file():
            password = "test"
            g.connection = create_connection(password)
        else:
            with open(db_password, "r") as password_file:
                password = password_file.readline()
                g.connection = create_connection(password)

    return g.connection


def close_connection(e=None):
    connection = g.pop("connection", None)

    if connection is not None:
        connection.close()


def init_connection(app):
    app.teardown_appcontext(close_connection)


@bp.cli.command("initialize")
def reset_database():
    connection = get_connection()
    transaction = connection.begin()
    try:
        connection.execute("DROP TABLE IF EXISTS sqli1_users;")
        connection.execute("DROP TABLE IF EXISTS sqli2_users;")
        connection.execute(
            """
        CREATE TABLE sqli1_users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(300) UNIQUE NOT NULL,
            password VARCHAR(300) NOT NULL
        );
        """
        )
        connection.execute(
            """
        CREATE TABLE sqli2_users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(300) UNIQUE NOT NULL,
            password VARCHAR(300) NOT NULL
        );
        """
        )
        connection.execute("INSERT INTO sqli1_users (username, password) VALUES ('administrator', 'password123')")
        transaction.commit()
    except Exception:
        transaction.rollback()
        print("transaction failed")
