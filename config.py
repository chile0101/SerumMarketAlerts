GET_PAIRS_API = "https://api.raydium.io/pairs"
RAYDIUM_RPC_MARKET_API = "https://api.raydium.io/cache/rpc/market"
RAYDIUM_RPC_AMM_API = "https://api.raydium.io/cache/rpc/amm"
DEXLAB_GET_PAIRS_API = "https://api.dexlab.space/v1/pairs"

TELE_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
TELE_TOKEN = "2079209599:AAEcwwdWgTnLD6Jr_C42h-W7DnKXN0zdxT4"

FIRST_CHAT_ID = "-508962559"
PRIVATE_CHAT_ID = "-1001358689192"
SERUM_CHAT_ID = "-1001409426229"
XNXX_GROUP = "-1001227796934"

RAYDIUM_PAIRS_DATA = 'data/raydium_pair.json'
DEXLAB_PAIRS_DATA = 'data/dexlab_market.json'
RAYDIUM_RPC_DATA = 'data/raydium_rpc.json'


class ChangeType:
    NEW_TOKEN = "New Token"
    UPDATED_INFO = "Updated Info"
    ADDED_POOL = "Added Pool"
    RAYDIUM_NEW_MARKET = "Raydium New Market"
