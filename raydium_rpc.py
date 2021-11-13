import json
import os
import random
import time

import backoff
import requests
from requests.exceptions import Timeout, HTTPError, RequestException

from config import TELE_TOKEN, TELE_URL, FIRST_CHAT_ID, RAYDIUM_RPC_DATA, RAYDIUM_RPC_AMM_API, ChangeType

DATA = {}
NO_PAIRS = 0


def controller(p, action):
    if action == "exception":
        requests.get(TELE_URL.format(TELE_TOKEN, FIRST_CHAT_ID, " is not working."))
    else:

        formatted_pair = "" \
                         f"{action} \n" \
                         f"market/amm: {p['pubkey']} \n"

        requests.get(TELE_URL.format(TELE_TOKEN, FIRST_CHAT_ID, formatted_pair))
        # time.sleep(60)
        # requests.get(TELE_URL.format(TELE_TOKEN, PRIVATE_CHAT_ID, formatted_pair))


def init():
    global DATA, NO_PAIRS
    if os.path.exists(RAYDIUM_RPC_DATA) and os.stat(RAYDIUM_RPC_DATA).st_size != 0:
        with open(RAYDIUM_RPC_DATA) as json_file:
            DATA = json.load(json_file)
            NO_PAIRS = len(DATA)
            print(f"Init DATA from FILE with {str(NO_PAIRS)} pairs.")
    else:
        # file not exists or empty -> init from api
        first_result = requests.get(RAYDIUM_RPC_AMM_API)
        if first_result.status_code == 200:
            for pair in first_result.json()['result']:
                DATA[pair['pubkey']] = pair
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
def scan():
    global DATA, NO_PAIRS
    while True:
        second_result = requests.get(RAYDIUM_RPC_AMM_API)
        if second_result.status_code == 200:
            NO_PAIRS = len(second_result.json()['result'])
            print("RPC pairs: " + str(NO_PAIRS))

            for pair in second_result.json()['result']:
                if pair['pubkey'] not in DATA:
                    controller(pair, ChangeType.RAYDIUM_NEW_MARKET)

        n_rand = random.randint(3, 5)
        # print(f'Waiting...{n_rand}s')
        time.sleep(n_rand)


def save_data():
    global DATA, NO_PAIRS
    json_obj = json.dumps(DATA)
    f = open(RAYDIUM_RPC_DATA, "w")
    f.write(json_obj)
    f.close()
    print(f"DATA saved with {NO_PAIRS} pairs.")


def main():
    print("Raydium RPC Scanner starting...")
    init()
    try:
        scan()
        save_data()
    except KeyboardInterrupt:
        save_data()
        print("KeyboardInterrupt")
    except Exception as e:
        controller(None, "exception")
        print(e)
        save_data()


if __name__ == '__main__':
    main()
