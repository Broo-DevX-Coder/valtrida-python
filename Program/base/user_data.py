# Variables for user data, such as API keys, user info, etc.

# == User Data Dicts ==
USER_LOCAL_INFO = {
    "name": '',
    "id": '',
    "auths_tokens": []
}

USER_BINANCE_INFO = {
    "api_key": '',
    "api_secret": '',
    "user_id": '',
    "account_type": 'SPOT'
}

USER_OFFICIAL_ACCOUNT_INFO = {
    "email": '',
    "name": '',
    "token": '',
}


"""Class to set user data in a structured way, such as local info, Binance info, official account info, etc."""
def set_user_local_info(name: str, id: str):
    USER_LOCAL_INFO["name"] = name
    USER_LOCAL_INFO["id"] = id

def set_user_binance_info(api_key: str, api_secret: str, user_id: str, account_type: str):
    USER_BINANCE_INFO["api_key"] = api_key
    USER_BINANCE_INFO["api_secret"] = api_secret
    USER_BINANCE_INFO["user_id"] = user_id
    USER_BINANCE_INFO["account_type"] = account_type

def set_user_official_account_info(email: str, name: str, token: str):
    USER_OFFICIAL_ACCOUNT_INFO["email"] = email
    USER_OFFICIAL_ACCOUNT_INFO["name"] = name
    USER_OFFICIAL_ACCOUNT_INFO["token"] = token

def set_auth_tokens(auths_tokens: list):
    USER_LOCAL_INFO["auths_tokens"] = auths_tokens

class UserDataGet:
    """Class to get user data in a structured way, such as local info, Binance info, official account info, etc."""
    
    @staticmethod
    def get_user_local_info():
        return USER_LOCAL_INFO

    @staticmethod
    def get_user_binance_info():
        return USER_BINANCE_INFO

    @staticmethod
    def get_user_official_account_info():
        return USER_OFFICIAL_ACCOUNT_INFO