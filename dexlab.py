import json
import os
import random
import time

import backoff
import requests
from requests.exceptions import Timeout, HTTPError, RequestException

from config import TELE_URL, TELE_TOKEN, PRIVATE_CHAT_ID, DEXLAB_PAIRS_DATA, DEXLAB_GET_PAIRS_API

DATA = {}
NO_PAIRS = 0


class ChangeType:
    NEW_MARKET = "New Market"
    # UPDATED_INFO = "Updated Info"
    # ADDED_POOL = "Added Pool"


def controller(p, action):
    if action == "exception":
        requests.get(TELE_URL.format(TELE_TOKEN, PRIVATE_CHAT_ID, "Bot is not working."))
    else:

        formatted_pair = "" \
                         f"{action} \n" \
                         f"market: {p['market']} \n" \
                         f"coin: {p['coin']} \n" \
                         f"priceCurrency: {p['priceCurrency']}\n" \
                         f"address: {p['address']} \n" \
                         f"baseMint: {p['baseMint']} \n"

        requests.get(TELE_URL.format(TELE_TOKEN, PRIVATE_CHAT_ID, formatted_pair))


def init():
    global DATA, NO_PAIRS
    if os.path.exists(DEXLAB_PAIRS_DATA) and os.stat(DEXLAB_PAIRS_DATA).st_size != 0:
        with open(DEXLAB_PAIRS_DATA) as json_file:
            DATA = json.load(json_file)
            NO_PAIRS = len(DATA)
            print(f"Init DATA from FILE with {str(NO_PAIRS)} pairs.")
    else:
        # file not exists or empty -> init from api
        first_result = requests.get(DEXLAB_GET_PAIRS_API)
        if first_result.status_code == 200:
            for pair in first_result.json()['data']:
                DATA[pair['address']] = pair
            NO_PAIRS = len(DATA)
            print(f"Init DATA from API with {str(len(DATA))} pairs.")
        else:
            print("Status != 200")


def backoff_hdlr(details):
    print("Backing off {wait:0.1f} seconds after {tries} tries "
          "calling function {target} with args {args} and kwargs "
          "{kwargs}".format(**details))


@backoff.on_exception(backoff.expo, (Timeout, RequestException, HTTPError),
                      max_tries=10,
                      on_backoff=backoff_hdlr
                      )
def main():
    global DATA, NO_PAIRS
    while True:
        second_result = requests.get(DEXLAB_GET_PAIRS_API)
        if second_result.status_code == 200:
            NO_PAIRS = len(second_result.json()['data'])
            print("Dexlab pairs: " + str(NO_PAIRS))
            for pair in second_result.json()['data']:
                if pair['address'] in DATA:
                    continue
                else:
                    controller(pair, ChangeType.NEW_MARKET)
                    DATA[pair['address']] = pair

        time.sleep(random.randint(10, 20))


def save_data():
    global DATA, NO_PAIRS
    json_obj = json.dumps(DATA)
    f = open("MARKETS.json", "w")
    f.write(json_obj)
    f.close()
    print(f"DATA saved with {NO_PAIRS} pairs.")


def new_market_alert():
    init()
    try:
        main()
        save_data()
    except KeyboardInterrupt:
        save_data()
        print("KeyboardInterrupt")
    except Exception as e:
        controller(None, "exception")
        print(e)
        save_data()
