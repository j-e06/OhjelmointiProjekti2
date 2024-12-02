import json

import requests

BASE_URL = "http://127.0.0.1:5000/api/"


def check_if_valid(data):
    if data.status_code != 200:
        print(data.json)
        quit()

def main():

    response = requests.get(f"{BASE_URL}login?name=Janit&password=Pirkka")
    check_if_valid(response)

    game_id = response.json()['status'][-1]
    print(game_id)


main()