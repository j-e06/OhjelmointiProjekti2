import mariadb

from utils.database import execute_query
from geopy import distance

from utils.CONSTANTS import DEFAULT_AIRPORT_TYPE, DEFAULT_AIRPORT_COUNT


def create_game_airports(cursor: mariadb.Cursor):
    f"""
    
    Args:
        cursor:
    Returns:
            a list of all airports that are in EU and are of type large_airport
            limited to a count of 30, and randomized per running of function            
    """
    sql = f"SELECT * from airport where continent = 'EU' AND type = '{DEFAULT_AIRPORT_TYPE}' " \
          f"ORDER BY RAND() LIMIT {DEFAULT_AIRPORT_COUNT}"
    airports = execute_query(cursor, sql)
    return airports


def get_all_airports(cursor, game_id: int) -> list:
    """
    Returns all airports from database that can be found in the given airports list
    (airports table should only contain the idents (icao-codes) of the airports)
    """

    test = "SELECT airport.* FROM airport INNER JOIN game_airports ON airport.ident = game_airports.airport_id " \
           "WHERE game_airports.game_id = %s;"

    return execute_query(cursor, test, (game_id,))


def get_airport_info(cursor, code: str, game_id: int = None):
    """
    Gets information for the airport with the corresponding ICAO-code.
    If game_id is filled in, returns information for said airport from game_airports and airport tables.
    """
    if not valid_airport(cursor, code):
        return "Invalid ICAO-code"
    if game_id is None:
        sql = "SELECT * from airport where ident = %s"

        return execute_query(cursor, sql, (code,))

    else:
        sql = "SELECT game_airports.*, airport.* FROM game_airports INNER JOIN airport on " \
              "game_airports.airport_id = airport.ident WHERE game_airports.game_id = %s " \
              "AND game_airports.airport_id = %s"

        return execute_query(cursor, sql, (game_id, code,))


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


def accessible_airports(cursor, icao: str, fuel: float, game_id: int):
    """
    :param cursor:
    :param icao:
    :param fuel: The amount of range that can be flown to, float
    :return: a list of all airports that are in the range

    Args:
        game_id:
    """
    if not valid_airport(cursor, icao):
        return "Invalid ICAO-code"
    available = []
    airports = get_all_airports(cursor, game_id)
    for port in airports:
        distance_from_port = get_distance(cursor, icao, port['ident'])
        if fuel >= distance_from_port > 1:
            available.append(port)
    return True, available
