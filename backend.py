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
    run_sql_file(g.cursor, SQL_FILE_PATH)
    # run_sql_file(g.cursor, RESET_FILE_PATH)


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
        return jsonify({"error": f"Unables to get information for said airport for game {game_id}"}), 400

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


app.run(debug=True)
