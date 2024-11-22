from flask import Flask, request, jsonify, g

from utils.database import Database, run_sql_file

from utils.game import *
from utils.lootboxes import *
from utils.airports import *


config = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "project",
    "user": "root",
    "password": "potatoman",
    "autocommit": True
}

SQL_FILE_PATH = "C:/Users/janie/PycharmProjects/OhjelmointiProjekti2/utils/database_creation.sql"
RESET_FILE_PATH = "C:/Users/janie/PycharmProjects/OhjelmointiProjekti2/utils/reset_db.sql"



app = Flask(__name__)

@app.before_request
def setup_db():
    db = Database(**config)
    g.db = db


    g.cursor = db.__enter__()
    run_sql_file(g.cursor, SQL_FILE_PATH)
    # run_sql_file(g.cursor, RESET_FILE_PATH)

@app.route('/api/create_new_game', methods=['GET'])
def create_new_name():

    cursor = g.cursor

    args = request.args
    name = args.get("name")
    password = args.get("password")
    if not name or not password:
        return jsonify({"error": "Missing 'name' or 'password'"}), 400
    # print(cursor)
    # return f"<li>{type(cursor), str(cursor)}</li>"
    game_id = create_game(cursor, name, password)
    return jsonify({"game_id": game_id}), 200


app.run(debug=True)