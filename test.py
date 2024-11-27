from utils.airports import *
from utils.database import *

import mariadb
config = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "project",
    "user": "root",
    "password": "potatoman"
}


with Database(**config) as cursor:
    #run_sql_file(cursor, "C:/Users/janie/PycharmProjects/OhjelmointiProjekti2/utils/database_creation.sql")


    game_id = 1

    print(get_airport_info(cursor, "EFHK", game_id))