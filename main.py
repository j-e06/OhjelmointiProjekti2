from utils.database import *
from utils.airports import *
import mariadb
config = {
    "host": "127.0.0.1",
    "port": 3307,
    "database": "project",
    "user": "root",
    "password": "root",
    "autocommit": True
}

SQL_FILE_PATH = "C:/Users/janie/PycharmProjects/OhjelmointiProjekti2/database_creation.sql"


def main(connection_config, file_path):
    with Database(**connection_config) as cursor:
        sql_file_path = ""
        run_sql_file(cursor, file_path)

        print(f"Database setup complete.")


if __name__ == "__main__":
    main(config, SQL_FILE_PATH)
