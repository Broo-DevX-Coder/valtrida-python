# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
import hashlib
import hmac
import time
import aiohttp

# == local ==
from core import error


# ==================================================================
# Helper functions
# ==================================================================

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"API.b_accont.{source}", msg)

def create_signature(params, secret):
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


# ==================================================================
# Vars
# ==================================================================
URL = "https://api.binance.com"


# ==================================================================
# functions
# ==================================================================  
async def get_account_info(api_key: str, api_secret: str, session: aiohttp.ClientSession = None):
    endpoint = "/api/v3/account"
    url = URL + endpoint

    params = {
        "timestamp": int(time.time() * 1000)
    }
    params["signature"] = create_signature(params, api_secret)

    headers = {
        "X-MBX-APIKEY": api_key
    }

    close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        close_session = True

    try:
        async with session.get(url, headers=headers, params=params) as response:
            status = response.status

            if status == 200:
                r = await response.json()
                if str(r) == "{}" or not r.get("code"):
                    return True, r

            elif status == 400:
                error_("SECREAT_KEY_ERROR","get_account_info","This secret key is unacceptable with api-key")
                return False, "SECREAT_KEY_ERROR"

            elif status == 401:
                error_("INVALID_API_KEY","get_account_info","invalid api-key or missing permissions")
                return False, "INVALID_API_KEY"

            else:
                error_(f"CONNECTION_{status}","get_account_info",f"Server Return Error Code: {status}")
                return False, "UNKNON_ERROR"

    except Exception as e:
        error_(e,"get_account_info",str(e))
        return False, "CONNECTION_ERROR"

    finally:
        if close_session:
            await session.close()


async def get_prices(session: aiohttp.ClientSession = None):
    url = URL + "/api/v3/ticker/price"

    close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        close_session = True

    try:
        async with session.get(url) as response:
            status = response.status

            if status == 200:
                r = await response.json()
                if isinstance(r, list):
                    return {x["symbol"]: float(x["price"]) for x in r}
                else:
                    error_(f"CONNECTION_{status}","get_prices",f"Server Return Error Code: {status}")
                    return False
            else:
                error_(f"CONNECTION_{status}","get_prices",f"Server Return Error Code: {status}")
                return False

    except Exception as e:
        error_(e,"get_prices",str(e))
        return False

    finally:
        if close_session:
            await session.close()


async def get_total_balance_in_usdt(api_key, api_secret, session: aiohttp.ClientSession = None):

    account = await get_account_info(api_key, api_secret, session)
    if account[0] is True:
        balances = account[1].get("balances")
    else:
        return False

    prices = await get_prices(session)
    if prices is False:
        return False

    total_usdt = 0.0
    free_amount = 0.0
    locked_amount = 0.0

    for b in balances:
        asset = b["asset"]
        free = float(b["free"])
        locked = float(b["locked"])
        amount = free + locked

        if amount == 0:
            continue

        if asset == "USDT":
            total_usdt += amount
            free_amount += free
            locked_amount += locked
        else:
            symbol = asset + "USDT"
            if symbol in prices:
                price = prices[symbol]
                total_usdt += amount * price
                free_amount += free * price
                locked_amount += locked * price
            else:
                # No direct USDT pair available
                pass

    return total_usdt, free_amount, locked_amount, balances