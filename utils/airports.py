from utils.database import execute_query
from geopy import distance


def create_game_airports(cursor, wanted_info: str = "*"):
    f"""
    
    Args:
        cursor:
        wanted_info:  
         SELECT * from airport
         
        With params:
        SELECT wanted_info from airport where params
        For example:
        SELECT (default value is *) from airport where continent = 'EU' AND type ='large_airport';
        
        or
        
        SELECT wanted_info from airport where continent = 'EU' AND type ='large_airport'
        
        This set of airports will be used for the current game and everything related to it!
    Returns:
            a list of all airports that fit the given criteria
    """
    sql = "SELECT"
    if wanted_info is not None:
        sql += wanted_info
    else:
        sql += " *"
    sql += " from airport WHERE continent = 'EU' AND type ='large_airport'"

    return execute_query(cursor, sql)


def get_all_airports(cursor, airports: list) -> list:
    """
    Returns all airports from database that can be found in the given airports list
    (airports table should only contain the idents (icao-codes) of the airports)
    """
    sql = "SELECT * from airport where continent = 'EU' AND type ='large_airport'"

    return execute_query(cursor, sql)


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


def accessible_airports(cursor, icao: str, p_range: float):
    """
    :param cursor:
    :param icao:
    :param p_range: The amount of range that can be flown to, float
    :return: a list of all airports that are in the range
    """
    if not valid_airport(cursor, icao):
        return "Invalid ICAO-code"
    available = []
    airports = get_all_airports(cursor)
    for port in airports:
        distance_from_port = get_distance(cursor, icao, port['ident'])
        if p_range >= distance_from_port > 1:
            available.append(port)
    return available
