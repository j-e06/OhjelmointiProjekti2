from utils.database import *
from utils.airports import *
import mariadb

from utils.game import *

config = {
    "host": "127.0.0.1",
    "port": 3307,
    "database": "project",
    "user": "root",
    "password": "root",
    "autocommit": True
}

SQL_FILE_PATH = "C:/Users/janie/PycharmProjects/OhjelmointiProjekti2/utils/database_creation.sql"
RESET_FILE_PATH = "C:/Users/janie/PycharmProjects/OhjelmointiProjekti2/utils/reset_db.sql"


def main(connection_config, file_path):
    with Database(**connection_config) as cursor:

        # RESET TABLES IN DB.
        run_sql_file(cursor, RESET_FILE_PATH)

        run_sql_file(cursor, SQL_FILE_PATH)

        print(f"Database setup complete.")

        print("Testing creation of game_airports...")
        name = "Jani"
        password = "Test"

        game_id = create_game(cursor, name, password)

        test = fly(cursor, game_id, "EFHK")

        print(test)


if __name__ == "__main__":
    main(config, SQL_FILE_PATH)
