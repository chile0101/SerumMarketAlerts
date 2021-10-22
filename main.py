import time

import requests
from requests import Timeout, HTTPError

GET_PAIRS_API = "https://api.raydium.io/pairs"
TELE_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
TELE_TOKEN = "2079209599:AAEcwwdWgTnLD6Jr_C42h-W7DnKXN0zdxT4"
CHAT_ID = "-771318813"
DATA = {}

first_result = requests.get(GET_PAIRS_API)
if first_result.status_code == 200:
    print("Init with number of pairs: " + str(len(first_result.json())))
    for pair in first_result.json():
        DATA[pair['market']] = pair
else:
    print("Status != 200")

while True:
    try:
        second_result = requests.get(GET_PAIRS_API)
        if second_result.status_code == 200:
            print("Number of pairs: " + str(len(second_result.json())))
            for pair in second_result.json():
                if pair['market'] in DATA:
                    continue
                else:
                    formatted_pair = "" \
                                     f"name: {pair['name']} \n" \
                                     f"pair_id: {pair['pair_id']} \n" \
                                     f"market: {pair['market']} \n" \
                                     f"price: {pair['price']} \n" \
                                     f"amm_id: {pair['amm_id']} \n" \
                                     f"official: {pair['official']} \n" \
                                     f"liquidity: {pair['liquidity']} \n" \
                                     f"token_amount_coin: {pair['token_amount_coin']} \n" \
                                     f"token_amount_lp: {pair['token_amount_lp']} \n" \
                                     f"token_amount_pc: {pair['token_amount_pc']} \n" \
                                     f"apy: {pair['apy']} \n"
                    requests.get(TELE_URL.format(TELE_TOKEN, CHAT_ID, formatted_pair))
                    DATA[pair['market']] = pair
        else:
            print("Status != 200")

    except Timeout as e:
        print("Timeout exception", e)
    except HTTPError as e:
        print("HttpError exception", e)
        raise SystemExit(e)

    time.sleep(3)

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
# them thong tin ve liquidity
# call api in chat
