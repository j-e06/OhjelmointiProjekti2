import mariadb
from random import sample, shuffle

from utils.database import execute_query
from utils.airports import get_airport_info, valid_airport
# from utils.game import get_game_details
from utils.CONSTANTS import DEFAULT_AIRPORT_COUNT, LOOTBOX_COST_MONEY, LOOTBOX_COST_FUEL


def open_port_lootbox(cursor, icao_code, game_id, open_type):
    from utils.game import get_game_details

    airport_details = get_airport_info(cursor, icao_code, game_id)


    if len(airport_details) == 0:
        return False, "No information found for given airport. Probably not in our game."
    airport_details = airport_details[0]
    if airport_details['lootbox_status'] != 0:
        return False, "Lootbox already opened."

    # lootbox has not been opened yet and we can continue.

    lootbox_id = airport_details['lootbox_id']

    game_details = get_game_details(cursor, game_id)[0]

    if open_type not in ["money", "fuel"]:
        return False, "Invalid open type."
    if open_type == "money":
        if game_details['money'] - LOOTBOX_COST_MONEY < 0:
            # can't afford it.
            return False, "Cannot afford to open lootbox with money."
    else:
        if game_details['fuel'] - LOOTBOX_COST_FUEL < 0:
            return False, "Cannot afford to open lootbox with fuel."


    # we know the lootbox has not been opened, AND we have enough for it in either money, or fuel.

    lootbox_info = get_lootbox(cursor, lootbox_id)

    print(lootbox_info)



def get_lootboxes(cursor):
    """
    :param cursor:
    :return
    List: Returns a list with dictionary key, value pairs for all goals:
    """
    sql = "SELECT * from lootboxes"
    return execute_query(cursor, sql)


def get_lootbox(cursor, primary_id: int):
    """

    :param cursor:
    :param primary_id: Primary id for the specific goal to be returned
    :return: data for the goal with the given primary_id
    """
    sql = "SELECT * from lootboxes where id = %s"

    result = execute_query(cursor, sql, (primary_id,))
    return result


def create_lootboxes(cursor: mariadb.Cursor, game_id, game_airports: list):
    sql = "SELECT id,spawn_weight, goal_name from lootboxes"

    results = execute_query(cursor, sql)

    weighted_ids = []
    id_to_name = {}
    diamond_id = 0
    for lootbox in results:
        lootbox_id = lootbox['id']
        weight = lootbox['spawn_weight']
        goal_name = lootbox['goal_name']
        if goal_name == "Diamond":
            diamond_id = lootbox_id
        weighted_ids.extend([lootbox_id] * weight)
        id_to_name[lootbox_id] = goal_name


    if diamond_id in weighted_ids:
        weighted_ids = [lootbox_id for lootbox_id in weighted_ids if lootbox_id != diamond_id]

    selected_ids = sample(weighted_ids, DEFAULT_AIRPORT_COUNT - 1)
    selected_ids.append(diamond_id)

    # the above is some probability magic done by the one and only, chatGPT
    # not entirely certain how it works.

    shuffle(selected_ids)

    t = []
    for i in range(DEFAULT_AIRPORT_COUNT):
        t.append(selected_ids[i])
    test_sql = "INSERT INTO game_airports (game_id, airport_id, lootbox_status, lootbox_id) VALUES"
    for airport, lootbox_id in zip(game_airports, t):
        placeholder = f"({game_id}, '{airport['ident']}', {False}, {lootbox_id}),"
        test_sql += placeholder

    test_sql = test_sql[:-1]  # removes trailing , character
    execute_query(cursor, test_sql, fetch=False)
