#crear connection para la base de datos
import psycopg2
from config import db_config


def get_connected():
    if not db_config["password"]:
        raise ValueError("error to connect to databse")

    try:
        conn=psycopg2.connect(
            host = db_config["host"],
            port = db_config["port"],
            user = db_config["user"],
            password = db_config["password"],
            database = db_config["database"]

        )

        print(f"successfull to connected")
        return conn

    except psycopg2.Error as e:
        print(f"error to connect to database: {e}")
        return False