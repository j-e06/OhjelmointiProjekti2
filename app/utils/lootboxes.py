import mariadb
from random import sample, shuffle

from utils.database import execute_query
from utils.airports import get_airport_info, valid_airport
# from utils.game import get_game_details
from utils.CONSTANTS import DEFAULT_AIRPORT_COUNT, LOOTBOX_COST_MONEY, LOOTBOX_COST_FUEL


def open_port_lootbox(cursor, game_id, open_type):
    from utils.game import get_game_details, save_game

    # Retrieve game details
    game_details = get_game_details(cursor, game_id)[0]

    icao_code = game_details['location']
    airport_details = get_airport_info(cursor, icao_code, game_id)

    if not airport_details:
        return False, "No information found for the given airport. Probably not in our game."

    airport_details = airport_details[0]
    if airport_details['lootbox_status'] != 0:
        return False, "Lootbox already opened."

    lootbox_id = airport_details['lootbox_id']

    money = game_details['money']
    fuel = game_details['fuel']
    diamond = game_details.get('diamond', 0)  # Ensure diamond handling
    updates = {}  # Dictionary to track column updates (prevents duplicates)

    # Handle opening type costs
    if open_type not in ["money", "fuel"]:
        return False, "Invalid open type."

    if open_type == "money":
        if money - LOOTBOX_COST_MONEY < 0:
            return False, "Cannot afford to open lootbox with money."
        else:
            money -= LOOTBOX_COST_MONEY
            updates["money"] = money
    else:  # open_type == "fuel"
        if fuel - LOOTBOX_COST_FUEL < 0:
            return False, "Cannot afford to open lootbox with fuel."
        else:
            fuel -= LOOTBOX_COST_FUEL
            updates["fuel"] = fuel

    # Retrieve lootbox info
    lootbox_info = get_lootbox(cursor, lootbox_id)[0]
    reward = int(lootbox_info['reward'])

    # Process lootbox rewards
    if reward > 1:
        money += reward
        updates["money"] = money  # Ensure we overwrite the previous money update if needed
        line = f"You found a {lootbox_info['goal_name']}, gaining {reward} euros! New balance: {money}."
    elif reward == 1:
        diamond += 1
        updates["diamond"] = diamond
        line = "Congratulations! You have found the diamond! Proceed back to the starting airport."
    elif reward == 0:
        line = "You found milk, nothing happens."
    elif reward == -1:
        money = 0
        updates["money"] = money  # Overwrite any previous money update
        line = "Oh no! You've found a robber! They've stolen all of your money."

    # Save changes to the game table
    to_update = tuple(updates.keys())
    information = tuple(updates.values())
    result = save_game(cursor, game_id, to_update, information, fuel=LOOTBOX_COST_FUEL if "fuel" in updates.keys() else None, lootbox=True)

    # Update game_airports table to mark the lootbox as opened
    sql = "UPDATE game_airports SET lootbox_status = %s WHERE game_id = %s AND airport_id = %s"
    execute_query(cursor, sql, (1, game_id, icao_code), fetch=False)

    if result[0]:
        return True, line
    else:
        return False, result[1]


def get_lootbox(cursor, lootbox_id: int):
    """

    :param cursor:
    :param primary_id: Primary id for the specific goal to be returned
    :return: data for the goal with the given primary_id
    """
    sql = "SELECT * from lootboxes where id = %s"

    result = execute_query(cursor, sql, (lootbox_id,))
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
