from utils.database import *
from utils.airports import *
import mariadb
config = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "project",
    "user": "root",
    "password": "potatoman",
    "autocommit": True
}

def main():
    with Database(config) as cursor:
        pass


