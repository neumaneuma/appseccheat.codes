from flask import g
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    if "engine" not in g:

        with open("/run/secrets/db-password", "r") as password_file:
            database_type = "mysql"
            connector = "mysqlconnector"
            user = "root"
            password = password_file.readline()
            host = "db"
            port = "3306"
            database_name = "appsecdb"
            g.engine = create_engine(
                f"{database_type}+{connector}://{user}:{password}@{host}:{port}/{database_name}",
                echo=True,
            )

    # Create database session
    # Session = sessionmaker(bind=db)
    # session = Session()
    return g.engine


def get_connection():
    if "cursor" not in g:
        with open("/run/secrets/db-password", "r") as password_file:
            g.connection = mysql.connector.connect(
                user="root",
                password=password_file.readline(),
                host="db",
                database="appsecdb",
            )

    return g.connection


def close_connection(e=None):
    connection = g.pop("connection", None)

    if connection is not None:
        connection.close()


def init_connection(app):
    app.teardown_appcontext(close_connection)


def reset_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS sqli1_users;")
    cursor.execute("DROP TABLE IF EXISTS sqli2_users;")
    cursor.execute(
        """
    CREATE TABLE sqli1_users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(300) UNIQUE NOT NULL,
        password VARCHAR(300) NOT NULL
    );
    """
    )
    cursor.execute(
        """
    CREATE TABLE sqli2_users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(300) UNIQUE NOT NULL,
        password VARCHAR(300) NOT NULL
    );
    """
    )
    cursor.execute(
        "INSERT INTO sqli1_users (username, password) VALUES ('administrator', 'password123')"
    )
    connection.commit()
