from utils.database import *
from utils.lootboxes import *
from utils.airports import *


def get_game_details(cursor : mariadb.Cursor, game_id: int):
    """
    Returns all information for given game

    Returns None if game not found
    """

    sql = "SELECT * from game where game_id = %s"

    result = execute_query(cursor, sql,(game_id,))

    if len(result) == 0:
        return None
    else:
        return result

def save_game(cursor: mariadb.Cursor, **details):
    pass

def create_game(cursor: mariadb.Cursor, name, password) -> int:
    fuel = 1500 # KM static starting value
    money = 500 # EURO static starting value

    game_airports = create_game_airports(cursor)

    starting_airport = choice(game_airports)
    location = starting_airport

    fuel_used = 0.0
    lootboxes_opened = 0
    flights_taken = 0

    diamond = 0
    sql = (
        "INSERT INTO game (name, password, starting_airport, location, money, fuel, fuel_used, lootboxes_opened, flights_taken, diamond) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (
    name, password, starting_airport['ident'], location['ident'], money, fuel, fuel_used, lootboxes_opened, flights_taken, diamond)
    #test

    #print(data)
    execute_query(cursor,sql,data, fetch=False)
    game_id = cursor.lastrowid

    create_lootboxes(cursor, game_id, game_airports)

    return game_id
