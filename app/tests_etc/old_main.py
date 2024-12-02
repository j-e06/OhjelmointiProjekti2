import json
from flask import Flask, request

from utils.database import Database, execute_query, run_sql_file
# from utils.airports import accessible_airports, get_distance, valid_airport, get_airport_info, \
#    get_all_airports, create_game_airports
import mariadb

from utils.game import get_game_details, create_game, fly, save_game, check_game_state, buy_fuel


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


def main(connection_config, file_path, reset_path):
    with Database(**connection_config) as cursor:
        # return cursor
        # RESET TABLES IN DB.
        # run_sql_file(cursor, reset_path)

        run_sql_file(cursor, file_path)

        print(f"Database setup complete.")

        print("Testing creation of game...")
        name = "Jani"
        password = "Test"

        game_id = create_game(cursor, name, password)

        #game_id = 1

        # test = fly(cursor, game_id, "EFHK")

        result = buy_fuel(cursor, game_id, 500)
        if result:
            print("Fuel purchase successful.")
        else:
            print(result)


if __name__ == "__main__":
    main(config, SQL_FILE_PATH, RESET_FILE_PATH)
