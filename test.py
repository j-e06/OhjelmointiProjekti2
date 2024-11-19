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
    result = accessible_airports(cursor, "EFHK", 2500)
    print(result)