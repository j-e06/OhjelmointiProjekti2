import mariadb

from utils.database import execute_query
from geopy import distance


def create_game_airports(cursor: mariadb.Cursor):
    f"""
    
    Args:
        cursor:
        game_id:
    Returns:
            a list of all airports that are in EU and are of type large_airport
            
    """
    sql = "SELECT * from airport where continent = 'EU' AND type = 'large_airport' ORDER BY RAND() LIMIT 30"
    airports = execute_query(cursor,sql)
    return airports

    #do the below in create_game()

    #insert_sql = "INSERT INTO game_airports(game_id, airport_id, lootbox_status, lootbox_id) ("
    #for airport in airports:
    #    airport_id = airport['ident']
    #    lootbox_id = create_lootbox(cursor)
    #    insert_sql += f"{game_id, airport_id, False, lootbox_id}"
#
    #insert_sql += ")"
    #return execute_query(cursor, insert_sql)
    #insert_sql = ("INSERT INTO game_airports (game_id, airport_id, lootbox_status, lootbox_id) VALUES ("
    #              "%s)")
    #inserting into game_airports table based on the game_id given

def get_all_airports(cursor, game_id: int) -> list:
    """
    Returns all airports from database that can be found in the given airports list
    (airports table should only contain the idents (icao-codes) of the airports)
    """
    #test

    test = "SELECT airport.* FROM airport INNER JOIN game_airports ON airport.ident = game_airports.airport_id WHERE game_airports.game_id = %s;"
    sql = "SELECT * from airport where continent = 'EU' AND type ='large_airport'"

    return execute_query(cursor, test,(game_id,))


def get_airport_info(cursor, code: str):
    """
    Gets information for the airport with the corresponding ICAO-code.
    """
    if not valid_airport(cursor, code):
        return "Invalid ICAO-code"
    sql = "SELECT * from airport where ident = %s"

    return execute_query(cursor, sql, (code,))


def valid_airport(cursor, icao: str):
    """

    :param cursor:
    :param icao:
    :return: Returns True or False depending on if the ICAO-code can be found
    in the airports table.
    """
    sql = "SELECT * from airport where ident = %s"

    result = execute_query(cursor, sql, (icao,))

    if len(result) == 0:
        return False
    else:
        return True


def get_distance(cursor, icao1: str, icao2: str):
    """

    :param cursor:
    :param icao1: ICAO-code for the first airport
    :param icao2: ICAO-code for the second airport
    :return: The distance between the first and second airport
    """
    if not valid_airport(cursor, icao1) or not valid_airport(cursor, icao2):
        return "Invalid ICAO-codes."

    airport1 = get_airport_info(cursor, icao1)[0]
    airport2 = get_airport_info(cursor, icao2)[0]
    a_xy = (airport1["latitude_deg"], airport1["longitude_deg"])
    b_xy = (airport2["latitude_deg"], airport2["longitude_deg"])

    return distance.distance(a_xy, b_xy).km


def accessible_airports(cursor, icao: str, fuel: float, game_id:int):
    """
    :param cursor:
    :param icao:
    :param fuel: The amount of range that can be flown to, float
    :return: a list of all airports that are in the range
    """
    if not valid_airport(cursor, icao):
        return "Invalid ICAO-code"
    available = []
    airports = get_all_airports(cursor, game_id)
    for port in airports:
        distance_from_port = get_distance(cursor, icao, port['ident'])
        if fuel >= distance_from_port > 1:
            available.append(port)
    return available
