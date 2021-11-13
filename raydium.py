import json
import os
import random
import time

import backoff
import requests
from requests.exceptions import Timeout, HTTPError, RequestException

from config import TELE_TOKEN, TELE_URL, FIRST_CHAT_ID, PRIVATE_CHAT_ID, RAYDIUM_PAIRS_DATA, GET_PAIRS_API

DATA = {}
NO_PAIRS = 0


class ChangeType:
    NEW_TOKEN = "New Token"
    UPDATED_INFO = "Updated Info"
    ADDED_POOL = "Added Pool"


def controller(p, action):
    if action == "exception":
        requests.get(TELE_URL.format(TELE_TOKEN, FIRST_CHAT_ID, " is not working."))
    else:

        formatted_pair = "" \
                         f"{action} \n" \
                         f"name: {p['name']} \n" \
                         f"market: {p['market']} \n" \
                         f"pairs: {p['pair_id']}\n" \
                         f"price: {p['price']} \n" \
                         f"amm_id: {p['amm_id']} \n" \
                         f"token_amount_coin: {p['token_amount_coin']} \n" \
                         f"token_amount_pc: {p['token_amount_pc']} \n"

        requests.get(TELE_URL.format(TELE_TOKEN, FIRST_CHAT_ID, formatted_pair))
        # time.sleep(60)
        # requests.get(TELE_URL.format(TELE_TOKEN, PRIVATE_CHAT_ID, formatted_pair))

        # if action in (ChangeType.NEW_TOKEN, ChangeType.UPDATED_INFO, ChangeType.ADDED_POOL):
        #     formatted_pair = "" \
        #                      f"token: {p['name'].split('-')[0]} \n" \
        #                      f"address: {p['pair_id'].split('-')[0]}\n" \
        #                      f"market: {p['market']} \n" \
        #                      f"price: {p['price']} \n"
        # time.sleep(60)
        # requests.get(TELE_URL.format(TELE_TOKEN, SERUM_CHAT_ID, formatted_pair))
        # time.sleep(60)
        # requests.get(TELE_URL.format(TELE_TOKEN, XNXX_GROUP, formatted_pair))


def init():
    global DATA, NO_PAIRS
    if os.path.exists(RAYDIUM_PAIRS_DATA) and os.stat(RAYDIUM_PAIRS_DATA).st_size != 0:
        with open(RAYDIUM_PAIRS_DATA) as json_file:
            DATA = json.load(json_file)
            NO_PAIRS = len(DATA)
            print(f"Init DATA from FILE with {str(NO_PAIRS)} pairs.")
    else:
        # file not exists or empty -> init from api
        first_result = requests.get(GET_PAIRS_API)
        if first_result.status_code == 200:
            for pair in first_result.json():
                DATA[pair['amm_id']] = pair
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
        second_result = requests.get(GET_PAIRS_API)
        if second_result.status_code == 200:
            NO_PAIRS = len(second_result.json())
            print("Raydium pairs: " + str(NO_PAIRS))
            for pair in second_result.json():
                if pair['amm_id'] in DATA:
                    alr_pair = DATA[pair['amm_id']]
                    DATA[pair['amm_id']] = pair
                    if pair['token_amount_pc'] > 100 and pair['token_amount_pc'] > 10 * alr_pair['token_amount_pc']:
                        # controller(pair, ChangeType.ADDED_POOL)
                        continue
                    if pair['name'] != alr_pair['name']:
                        controller(pair, ChangeType.UPDATED_INFO)

                else:
                    DATA[pair['amm_id']] = pair

                    if pair['name'].split('-')[1] not in ['USDC', 'USDT']:
                        print(f'Ignore new token - not USD pair: {pair["name"]}')
                        # continue
                    if pair['token_amount_pc'] < 300:
                        print(f'Ignore new token - pool less than 300: {pair["name"]}')
                        # continue

                    controller(pair, ChangeType.NEW_TOKEN)
        n_rand = random.randint(3, 5)
        # print(f'Waiting...{n_rand}s')
        time.sleep(n_rand)


def save_data():
    global DATA, NO_PAIRS
    json_obj = json.dumps(DATA)
    f = open(RAYDIUM_PAIRS_DATA, "w")
    f.write(json_obj)
    f.close()
    print(f"DATA saved with {NO_PAIRS} pairs.")


def new_pool_alert():
    print("Raydium Scanner starting...")
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


if __name__ == '__main__':
    new_pool_alert()

# {
#         "name": "SLB-USDT",
#         "pair_id": "2uRFEWRBQLEKpLmF8mohFZGDcFQmrkQEEZmHQvMUBvY7-Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
#         "lp_mint": "DLYs4hagDBwMR5EBzsQYg83jAfWESREzqc91pDzoUdZ2",
#         "official": false,
#         "liquidity": 108706.41760912801,
#         "market": "46jD4hpmvUAbhKaoAjdzFkY82VW1j9SMTEYFGcTor8Ww",
#         "volume_24h": 8403.797601522352,
#         "volume_24h_quote": 8403.133515,
#         "fee_24h": 21.00949400380588,
#         "fee_24h_quote": 21.0078337875,
#         "volume_7d": 64151.82303654307,
#         "volume_7d_quote": 64151.44520499997,
#         "fee_7d": 160.3795575913577,
#         "fee_7d_quote": 160.37861301249993,
#         "price": 0.05511793024859677,
#         "lp_price": 0.047263659830055656,
#         "amm_id": "HdbmraBtbNKuLG5FqMZ4ocfHhCaAuV8qkTyE1iqs8BQu",
#         "token_amount_coin": 986076.418959576,
#         "token_amount_pc": 54350.49128,
#         "token_amount_lp": 2300000,
#         "apy": 7.05
# }

# TODO:
# add 3 button: solscan, dexlab chart
# call api in chat
# Viet them con new coingeco listing
# stuck
# or (pair['token_amount_coin'] > 100000
#     and pair['token_amount_coin'] > 30 * alr_pair['token_amount_coin']):
# compare dexlab price and ray.
# holders, verify web, tw,...
# link raydium to swap luon
# fix duplicate notify
