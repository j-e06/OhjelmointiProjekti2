import mariadb
from random import sample, shuffle

from utils.database import execute_query
from utils.airports import get_airport_info, valid_airport
# from utils.game import get_game_details
from utils.CONSTANTS import DEFAULT_AIRPORT_COUNT


# def open_lootbox(cursor, game_id):
#     game_details = get_game_details(cursor, game_id)[0]
#
#     airport_info = get_airport_info(cursor, game_id, game_details['ident'])
#
#     if airport_info['lootbox_status'] != 0:
#         return f"Lootbox for airport {airport_info['ident']} has already been opened. " \
#                f"Lootbox id was: {airport_info['lootbox_id']}"
#
#     lootbox_info = get_lootbox(cursor, airport_info['lootbox_id'])
#
#     lootbox_id = lootbox_info['id']
#
#     if lootbox_id == 1:
#         money = int(game_details['money']) + int(lootbox_info['reward'])
#         # topaz
#         pass
#     elif lootbox_id == 2:
#         money = int(game_details['money']) + int(lootbox_info['reward'])
#         # emerald
#         pass
#     elif lootbox_id == 3:
#         money = int(game_details['money']) + int(lootbox_info['reward'])
#         # ruby
#         pass
#     elif lootbox_id == 4:
#         # milk
#         # return "You found milk! Nothing happens."
#         pass
#     elif lootbox_id == 5:
#         # robber
#         money = 0
#
#         pass
#     elif lootbox_id == 6:
#         # diamond
#
#         pass
#     else:
#         # this should *not* be accessible.
#         pass



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
    return result if len(result) > 0 else False


def create_lootboxes(cursor: mariadb.Cursor, game_id, game_airports: list):
    sql = "SELECT id,spawn_weight, goal_name from lootboxes"

    results = execute_query(cursor, sql)

    weighted_ids = []
    id_to_name = {}

    for lootbox in results:
        lootbox_id = lootbox['id']
        weight = lootbox['spawn_weight']
        goal_name = lootbox['goal_name']
        weighted_ids.extend([lootbox_id] * weight)
        id_to_name[lootbox_id] = goal_name

    diamond_id = 6

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
