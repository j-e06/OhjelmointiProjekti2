import mariadb
from random import sample, shuffle, choice

from utils.database import execute_query

def get_lootboxes(cursor):
    """
    :param cursor:
    :return
    List: Returns a list with dictionary key, value pairs for all goals:
    """
    sql = "SELECT * from goals"
    return execute_query(cursor,sql)

def get_lootbox(cursor,primary_id: int):
    """

    :param cursor:
    :param primary_id: Primary id for the specific goal to be returned
    :return: data for the goal with the given primary_id
    """
    sql = "SELECT * from goals where id = %s"

    result = execute_query(cursor,sql,(primary_id,))
    return result if len(result) > 0 else "No goal with that primary id"

def create_lootboxes(cursor: mariadb.Cursor, game_id,game_airports:list):
    sql = "SELECT id,spawn_weight, goal_name from lootboxes"

    results = execute_query(cursor, sql)

    weighted_ids = []
    id_to_name = {}
    print(results)
    for lootbox_id, weight, goal_name in results:
        weighted_ids.extend([lootbox_id] * weight)
        id_to_name[lootbox_id] = goal_name

    diamond_id = 6

    if diamond_id in weighted_ids:
        weighted_ids = [lootbox_id for lootbox_id in weighted_ids if lootbox_id != diamond_id]

    selected_ids = sample(weighted_ids, 29)
    selected_ids.append(diamond_id)
    #test
    shuffle(selected_ids)

    t = []
    for i in range(30):
        t += selected_ids[i]
    test_sql = "INSERT INTO game_airports (game_id, airport_id, lootbox_status, lootbox_id) VALUES ("
    for airport, lootbox_id in enumerate(game_airports, t):
        placeholder = (game_id, airport['ident'], False, lootbox_id)
        test_sql += placeholder

    test_sql += ")"

    result = execute_query(cursor, test_sql)

