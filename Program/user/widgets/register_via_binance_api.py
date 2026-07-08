# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
import asyncio
import os
import random
import re

from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

# == local ==
from base.files_folders import USERS_FILE
from base.user_data import *
from Program.API.account import get_account_info
from user.local_cypher import CipherUserData

from core import AsyncController,log,error,critical_error,UserStream,SystemStream
from core.pop_messages import pup_message
from Styles.qss import QSS


# ==================================================================
# Helper classes and functions
# ==================================================================
def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"windows.main.{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.main.{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.main.{source}")

class RegisterViaBinanceAPI(QWidget):
    def __init__(self):
        super().__init__()
        self.size_ = [350, 245]

        self.setStyleSheet(QSS["BINANCE"])
        AsyncController.window_m(self,"add")

        # ---- set Page -----
        self.items = {}

        # === Register Page ===
        self.items["status"] = "normal"
        self.items["true_v"] = {"user_name":False,"API_key":False,"API_secreat":False,"password":False,"password-conf":False,"password_confirmed":True}
        self.items["user_name"] = QLineEdit(self)
        self.items["API_key"] = QLineEdit(self)
        self.items["API_secreat"] = QLineEdit(self)
        self.items["password"] = QLineEdit(self)
        self.items["password-conf"] = QLineEdit(self)
        self.items["sub_button"] = QPushButton("Register", self)

        self.items["user_name"].setPlaceholderText("Set User name")
        self.items["API_key"].setPlaceholderText("Binance API-key")
        self.items["API_secreat"].setPlaceholderText("Binance API-secreat (HMAC SHA256)")
        self.items["password"].setPlaceholderText("Set Password")
        self.items["password-conf"].setPlaceholderText("Confirm Password")

        self.items["password"].setEchoMode(QLineEdit.Password)
        self.items["password-conf"].setEchoMode(QLineEdit.Password)

        self.items["Y_first_item"] = 5
        self.items["user_name"].setGeometry(5,self.items["Y_first_item"],self.size_[0]-10,35)
        self.items["API_key"].setGeometry(5,self.items["Y_first_item"] + 40,self.size_[0]-10,35)
        self.items["API_secreat"].setGeometry(5,self.items["Y_first_item"] + 80,self.size_[0]-10,35)
        self.items["password"].setGeometry(5,self.items["Y_first_item"] + 120,self.size_[0]-10,35)
        self.items["password-conf"].setGeometry(5,self.items["Y_first_item"] + 160,self.size_[0]-10,35)
        self.items["sub_button"].setGeometry(5,self.items["Y_first_item"] + 200,self.size_[0]-10,35)

        # =========== Rigister Button enabling (signals) =========================
        self.items["user_name"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'user_name'))
        self.items["API_key"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'API_key'))
        self.items["API_secreat"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'API_secreat'))
        self.items["password"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'password'))
        self.items["password-conf"].textChanged.connect(lambda x: self.rigister_texts_slot(x,'password-conf'))

        # Rigister connection ============
        self.items["sub_button"].clicked.connect(lambda: asyncio.create_task(self.register()))

        self.items["sub_button"].setEnabled(False)


    # ======= Rigister button enabling (slot) ================
    def rigister_texts_slot(self,text:str,slot:str):
        self.items["true_v"][slot] = True if text and str(text).strip() and text is not None else False
        if slot == "password" or slot == "password-conf":
            self.items["true_v"]["password_confirmed"] = True if self.items["password"].text() == self.items["password-conf"].text() else False
        self.items["sub_button"].setEnabled(True if all(self.items["true_v"].values()) else False)

    def register_success(self,data):
        set_user_binance_info(
            api_key=data["api-key"], 
            api_secret=data["api-secreat"], 
            user_id=data["auther"]["UID"], 
            account_type=data["auther"]["accountType"]
        )
        set_user_local_info(
            name=data["user_name"], 
            id=str(data["id"])
        )
        UserStream.send({
            "type": "user_local_info",
            "event": "logged_in",
            "source": "user.widgets.login"
        })

    def ena(self):
        self.items["sub_button"].setEnabled(True)

    async def register(self):
        self.items["sub_button"].setEnabled(False)
        cipher = CipherUserData()
        user_name = self.items["user_name"].text()
        API_key = self.items["API_key"].text()
        API_secreat = self.items["API_secreat"].text()
        password = self.items["password"].text()
        
        if self.items["status"] == 'reset_accont':
            file_path = os.path.join(USERS_FILE,f"{user_name}.enc")
            if os.path.exists(file_path):
                os.remove(file_path)

        accont_info_api = await get_account_info(API_key,API_secreat)

        if len(password) < 8: 
            pup_message("Password Error","The password should be more then 8 degets",self.ena,"error")
            return
        elif self.is_valid_string(user_name) == False:
            pup_message("UserName Error","The user name shoud be just a digets or numbers or _",self.ena,"error")
            return
        elif accont_info_api[0] == False:
            if accont_info_api[1] == "INVALID_API_KEY":
                pup_message("API Key Error","This API Key invalide or has not the correct permitions\nApi type: HMAC-SHA256\nPermitions neded: Any IP Adress + Read Only",self.ena,"error")
            else:
                pup_message("API Secreat Error","The secreat key is not acceptable with this API Key",self.ena,"error")
            return

        else:
            us_id = random.randint(10_000_000,99_999_999)
            data = {
                "id":us_id,
                "user_name" : user_name,
                "api-key" : API_key,
                "api-secreat" : API_secreat,
                "auther":{
                    "UID" : str(accont_info_api[1].get("uid")),
                    "accountType":str(accont_info_api[1].get("accountType"))
            }}
            created = cipher.save_new_local_user(password,data)
            if created:
                pup_message("Seccess",f"User Created By user name:{user_name}\nClick ok to enter the program",lambda: self.register_success(data),"info")
            else:
                pup_message("Repeated user name","This username used in this device",self.ena,"error")

    # ======= Helpers ======================
    def is_valid_string(self,s: str) -> bool: 
        return bool(re.fullmatch(r"[A-Za-z0-9_]+", s))
    
    def closeEvent(self, event):
        event.accept()