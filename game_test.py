from flask import Flask, request, jsonify, g

from utils.database import Database, run_sql_file

from utils.game import create_game, get_game_details, fly, buy_fuel
from utils.lootboxes import open_port_lootbox
from utils.airports import get_airport_info, get_all_airports

import os
import json

from dotenv import load_dotenv

load_dotenv()
from utils.CONSTANTS import *

def game_test():
    config = {
        "host": os.getenv('host'),
        "port": int(os.getenv('port')),
        "database": os.getenv('database'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "autocommit": True
    }

    test = Database(**config)

    cursor = test.__enter__()
    name = "Jani"
    password = "potatoman"


    print("Creating game with starter values: "
          "Default fuel amount:", DEFAULT_FUEL_AMOUNT,
          "\nDefault money amount:", DEFAULT_MONEY_AMOUNT,
          "\nDefault airport amount:", DEFAULT_AIRPORT_COUNT,
          "\nDefault airport type", DEFAULT_AIRPORT_TYPE,
          "\nDefault fuel to money ratio:", FUEL_TO_MONEY_RATIO,
          "\nDefault lootbox money cost:", LOOTBOX_COST_MONEY,
          "\nDefault lootbox fuel cost:", LOOTBOX_COST_FUEL,
          "\n\n"
          )

    game_id = create_game(cursor, name, password)

    print("Game created, game_id: " + str(game_id))

    game_details = get_game_details(cursor, game_id)[0]

    print("All game details:", (detail + "\n" for detail in game_details))

    print(f"Opening current airports (icao_code: {game_details['location']} lootbox with money:")

    lootbox_result = open_port_lootbox(cursor, game_id, "money")

    if lootbox_result[0]:
        print(lootbox_result[1])


    print("Flying to nonexistent airport... ICAO-code: testi123")

    fly_result = fly(cursor, game_id, "testi123")

    print(fly_result)

    airports = get_all_airports(cursor, game_id)
    print("Flying to real airport.... ICAO-code= something that is in our game lol")
    real_fly_result = fly(cursor, game_id, airports[0]['ident'])

    print(real_fly_result)

    print("Opening lootbox with a nonexistent type: asd")

    box_result = open_port_lootbox(cursor, game_id, "asd")

    print(box_result)

    print("Opening lootbox with fuel...")

    print(open_port_lootbox(cursor,game_id,"fuel"))

    print("Trying to fly to same airport we are currently in....")

    game_details = get_game_details(cursor, game_id)[0]

    print(fly(cursor, game_id, game_details['location']))

    print("Buying fuel... 50 fuel should be 100 euros...")

    print(buy_fuel(cursor, game_id, game_details['money'] / 3))

    print("Buying fuel with an invalid amount.... 1500000000")

    print(buy_fuel(cursor, game_id, 150000000000))
    diamond_port = None
    for port in airports:
        port_info = get_airport_info(cursor, port['ident'], game_id)
        #print(port_info)

        if port_info[0]['lootbox_id'] == 6:
            diamond_port = port_info[0]


    print("Flying to airport that has the diamond..... Flying to port", diamond_port['ident'])

    print(fly(cursor,game_id,diamond_port['ident']))

    print("Opening lootbox to get diamond...")

    print(open_port_lootbox(cursor, game_id, "money"))

    print("Flying to starter airport.......")

    print(fly(cursor,game_id,game_details['starting_airport']))



game_test()
