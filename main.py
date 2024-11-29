from flask import Flask, request, jsonify, g

from utils.database import Database, run_sql_file

from utils.game import *
from utils.lootboxes import *
from utils.airports import *

import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv('host'),
    "port": int(os.getenv('port')),
    "database": os.getenv('database'),
    "user": os.getenv('user'),
    "password": os.getenv('password'),
    "autocommit": True
}

SQL_FILE_PATH = os.getenv('sql_file_path')
RESET_FILE_PATH = os.getenv('reset_file_path')

app = Flask(__name__)


@app.before_request
def setup_db():
    db = Database(**config)
    g.db = db

    g.cursor = db.__enter__()
    # run_sql_file(g.cursor, RESET_FILE_PATH)
    run_sql_file(g.cursor, SQL_FILE_PATH)


@app.route('/api/get_airport_information', methods=['get'])
def get_airport_information():
    cursor = g.cursor

    args = request.args
    icao = args.get("icao_code")
    game_id = int(args.get("game_id"))
    if not valid_airport(cursor, icao):
        return jsonify({"error": "Invalid ICAO-code"}), 400

    information = get_airport_info(cursor, icao, game_id)
    if len(information) > 0:
        return jsonify(information), 200
    else:
        return jsonify({"error": f"Unable to get information for said airport for game {game_id}"}), 400


@app.route('/api/create_new_game', methods=['GET'])
def create_new_game():
    cursor = g.cursor

    args = request.args
    name = args.get("name")
    password = args.get("password")
    if not name or not password:
        return jsonify({"error": "Missing 'name' or 'password'"}), 400

    game_id = create_game(cursor, name.strip(), password.strip())

    game_details = get_game_details(cursor, game_id)

    return jsonify(game_details), 200


@app.route('/api/save_game_details', methods=['GET'])
def save_game_details():
    cursor = g.cursor

    args = request.args

    game_id = int(args.get('game_id'))

    to_update = tuple(args.get('to_update').split(','))

    information = tuple(int(value) if value.isdigit() else value for value in args.get('information').split(","))
    result = save_game(cursor, game_id, to_update, information)
    # print(result)

    if result[0] is False:
        return jsonify({"error": result[1]}), 400
    else:
        return jsonify({"status": result[1]}), 200


@app.route('/api/open_lootbox', methods=['GET'])
def open_lootbox():
    cursor = g.cursor

    args = request.args

    game_id = int(args.get('game_id'))

    open_type = args.get('open_type')

    result = open_port_lootbox(cursor, game_id, open_type)

    if result[0] is False:
        return jsonify({"error": result[1]}), 400
    else:
        # Success!
        return jsonify({"status": result[1]}), 200


@app.route('/api/login', methods=['GET'])
def login():
    cursor = g.cursor

    args = request.args
    name = args.get("name")
    password = args.get("password")
    if name and password:
        if len(name) > 4 and len(password) > 4:
            result = login_to_game(cursor, name.strip(), password.strip())
            if result[0] is True:
                return jsonify({"status": result[1]}), 200
            else:
                return jsonify({"error": result[1]}), 200
    return jsonify({"error": "password or name is invalid"}), 400


@app.route('/api/register', methods=['GET'])
def register():
    cursor = g.cursor

    args = request.args

    name = args.get("name")
    password = args.get("password")

    if name and password:
        if len(name) > 4 and len(password) > 4:
            result = create_game(cursor, name, password)
            return jsonify(result), 200
    return jsonify({"error": "password or name is invalid"}), 400


@app.route('/api/refuel', methods=['GET'])
def refuel():
    cursor = g.cursor
    args = request.args
    game_id = int(args.get("game_id"))
    amount = int(args.get("amount"))
    if not game_id or not amount:
        return jsonify({"error": "Missing 'game_id' or 'amount'"}), 400
    result = buy_fuel(cursor, game_id, amount)
    if result[0]:
        return jsonify({"status": result[1]}), 200
    else:
        return jsonify({"error": result[1]}), 400

@app.route('/api/game_details', methods=['GET'])
def game_details():
    cursor = g.cursor
    args = request.args
    game_id = int(args.get("game_id"))
    if not game_id:
        return jsonify({"error": "Missing game_id"}), 400
    result = get_game_details(cursor, game_id)
    if result is None:
        return jsonify({"error": "Game not found"}), 400
    else:
        return jsonify({"status": result}), 200

@app.route('/api/check_accessible_airports', methods=['GET'])
def check_accessible_airports():
    cursor = g.cursor
    args = request.args
    game_id = int(args.get("game_id"))
    if not game_id:
        return jsonify({"error": "Missing game_id"}), 400
    airports = accessible_airports(cursor, game_id)
    if airports[0] is False:
        return jsonify({"error": airports[1]}), 400
    else:
        return jsonify({"status": airports[1]}), 200

@app.route('/api/check_distance', methods=['GET'])
def check_distance():
    cursor = g.cursor
    args = request.args
    icao1 = args.get("icao1")
    icao2 = args.get("icao2")
    result = check_distance(cursor, icao1, icao2)
    if result is False:
        return jsonify({"error": result[1]}), 400
    else:
        return jsonify({"status": result[1]}), 200

@app.route('/api/check_valid_airport', methods=['GET'])
def check_valid_airport():
    cursor = g.cursor
    args = request.args
    icao = args.get("icao")
    result = valid_airport(cursor, icao)
    if result is False:
        return jsonify({"error": result}), 400
    else:
        return jsonify({"status": result}), 200

@app.route('/api/lootbox', methods=['GET'])
def lootbox():
    cursor = g.cursor
    args = request.args
    lootbox_id = int(args.get("lootbox_id"))
    result = lootbox(cursor, lootbox_id)
    return jsonify({"status": result}), 200



if __name__ == "__main__":
    app.run(debug=True)
