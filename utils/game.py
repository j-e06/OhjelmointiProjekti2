from utils.database import execute_query
from utils.lootboxes import create_lootboxes
from utils.airports import create_game_airports, get_distance, valid_airport, accessible_airports

from random import choice

from utils.CONSTANTS import DEFAULT_FUEL_AMOUNT, DEFAULT_MONEY_AMOUNT, FUEL_TO_MONEY_RATIO



def get_game_details(cursor, game_id: int):
    """
    Returns all information for given game

    Returns None if game not found
    """

    sql = "SELECT * from game where game_id = %s"

    result = execute_query(cursor, sql, (game_id,))

    if len(result) == 0:
        return None
    else:
        return result


def create_game(cursor, name, password) -> int:
    fuel = DEFAULT_FUEL_AMOUNT  # KM static starting value
    money = DEFAULT_MONEY_AMOUNT  # EURO static starting value

    game_airports = create_game_airports(cursor)

    starting_airport = choice(game_airports)
    location = starting_airport

    fuel_used = 0.0
    lootboxes_opened = 0
    flights_taken = 0

    diamond = 0
    sql = (
        "INSERT INTO game (name, password, starting_airport, location, money, "
        "fuel, fuel_used, lootboxes_opened, flights_taken, diamond) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (name, password, starting_airport['ident'], location['ident'], money,
            fuel, fuel_used, lootboxes_opened, flights_taken, diamond)

    execute_query(cursor, sql, data, fetch=False)
    game_id = cursor.lastrowid

    create_lootboxes(cursor, game_id, game_airports)

    return game_id


def fly(cursor, game_id: int, icao_code: str):
    if not valid_airport(cursor, icao_code):
        return "Invalid ICAO-code."

    game_details = get_game_details(cursor, game_id)

    gid, name, password, starting_airport, location, money, fuel, fuel_used, lootboxes_opened, flights_taken, diamond = \
        game_details[0].values()

    if location == icao_code:
        return "Cannot fly to the same airport you are currently in."

    # Convert variables to appropriate types
    fuel = float(fuel)
    flights_taken = int(flights_taken)
    fuel_used = float(fuel_used)

    distance_between_ports = get_distance(cursor, location, icao_code)

    if fuel >= distance_between_ports > 1:

        # we can fly there

        fuel -= distance_between_ports

        location = icao_code

        flights_taken += 1

        fuel_used += distance_between_ports

        save_game(cursor, game_id, ('fuel', 'location', 'flights_taken', 'fuel_used'),
                  (fuel, location, flights_taken, fuel_used))
        return True
    else:
        return False


def save_game(cursor, game_id: int, to_update: tuple, information: tuple):
    # Ensure lengths of `to_update` and `information` match
    if len(to_update) != len(information):
        return False, "The lengths of 'to_update' and 'information' must match."

    # Construct SQL SET clauses
    set_clauses = [f"{column} = %s" for column in to_update]
    set_clauses_str = ', '.join(set_clauses)

    # Construct the query
    query = f"UPDATE game SET {set_clauses_str} WHERE game_id = %s;"
    params = (*information, game_id)


    execute_query(cursor, query, params=params, fetch=False)

    return True, "Success"


def check_game_state(cursor, game_id: int):
    game_details = get_game_details(cursor, game_id)

    gid, name, password, starting_airport, location, money, fuel, fuel_used, lootboxes_opened, flights_taken, \
    diamond = game_details[0].values()

    if location == starting_airport and diamond == 1:
        # We've WON!!!!!!
        pass

    available_airports = accessible_airports(cursor, location, fuel)

    if len(available_airports) == 0:
        # we've lost.
        pass


def buy_fuel(cursor, game_id: int, amount: int):
    """

    Args:
        amount:
        Amount of fuel to be bough in liters. So if you want to buy 500 liters of fuel, it would cost 1000 euros
        cursor:
        game_id:

    Returns:

    """

    game_details = get_game_details(cursor, game_id)[0]

    fuel = game_details['fuel']
    money = game_details['money']
    # print(money,fuel, amount, amount*2)
    if amount * 2 > money:
        return False

    new_fuel_count = fuel + amount
    new_money_count = money - amount * FUEL_TO_MONEY_RATIO

    result = save_game(cursor, game_id, ("fuel", "money"), (new_fuel_count, new_money_count))
    if result:
        return True
    else:
        return False
