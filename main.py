import json
import os
import random
import time

import backoff
import requests
from requests.exceptions import Timeout, HTTPError, RequestException

GET_PAIRS_API = "https://api.raydium.io/pairs"
TELE_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
TELE_TOKEN = "2079209599:AAEcwwdWgTnLD6Jr_C42h-W7DnKXN0zdxT4"
# CHAT_ID = "-771318813"
PRIVATE_CHAT_ID = "-622340650"
SERUM_CHAT_ID = "-1001409426229"
DATA_FILE_PATH = 'DATA.json'
DATA = {}
NO_PAIRS = 0


def send_to_tele(p, action):
    formatted_pair = "" \
                     f"{action} \n" \
                     f"name: {p['name']} \n" \
                     f"market: {p['market']} \n" \
                     f"price: {p['price']} \n" \
                     f"amm_id: {p['amm_id']} \n" \
                     f"token_amount_coin: {p['token_amount_coin']} \n" \
                     f"token_amount_pc: {p['token_amount_pc']} \n"
    print(formatted_pair)
    requests.get(TELE_URL.format(TELE_TOKEN, PRIVATE_CHAT_ID, formatted_pair))
    time.sleep(160)
    requests.get(TELE_URL.format(TELE_TOKEN, SERUM_CHAT_ID, formatted_pair))


def init():
    global DATA, NO_PAIRS
    if os.path.exists(DATA_FILE_PATH) and os.stat(DATA_FILE_PATH).st_size != 0:
        with open(DATA_FILE_PATH) as json_file:
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
                      max_tries=3,
                      on_backoff=backoff_hdlr
                      )
def main():
    global DATA, NO_PAIRS
    while True:
        second_result = requests.get(GET_PAIRS_API)
        if second_result.status_code == 200:
            NO_PAIRS = len(second_result.json())
            print("Current pairs: " + str(NO_PAIRS))
            for pair in second_result.json():
                if pair['amm_id'] in DATA:
                    alr_pair = DATA[pair['amm_id']]

                    if (pair['token_amount_pc'] > 10 and pair['token_amount_pc'] > 30 * alr_pair['token_amount_pc']) \
                            or (pair['token_amount_coin'] > 1000
                                and pair['token_amount_coin'] > 30 * alr_pair['token_amount_coin']):
                        send_to_tele(pair, "Add pool")

                    DATA[pair['amm_id']] = pair

                else:
                    send_to_tele(pair, "New pool")
                    DATA[pair['amm_id']] = pair

        time.sleep(random.randint(1, 10))


def save_data():
    global DATA, NO_PAIRS
    json_obj = json.dumps(DATA)
    f = open("DATA.json", "w")
    f.write(json_obj)
    f.close()
    print(f"DATA saved with {NO_PAIRS} pairs.")


if __name__ == '__main__':
    init()
    try:
        main()
    except (KeyboardInterrupt, Timeout, RequestException, HTTPError) as e:
        print("Exception")
        print(e)
        save_data()

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
