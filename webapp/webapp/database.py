from flask import g
from sqlalchemy import create_engine

from flask import Blueprint

bp = Blueprint("db", __name__)


def get_connection():
    if "connection" not in g:

        with open("/run/secrets/db-password", "r") as password_file:
            database_type = "mysql"
            connector = "mysqlconnector"
            user = "root"
            password = password_file.readline()
            host = "db"
            port = "3306"
            database_name = "appsecdb"
            engine = create_engine(
                f"{database_type}+{connector}://{user}:{password}@{host}:{port}/{database_name}",
                echo=True,
            )
            g.connection = engine.connect()

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
        connection.execute(
            "INSERT INTO sqli1_users (username, password) VALUES ('administrator', 'password123')"
        )
        transaction.commit()
    except:
        transaction.rollback()
        print("transaction failed")
