# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
import asyncio
import os

from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

# == local ==
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


# ==================================================================
# Main class
# ==================================================================
class LoggingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.size_ = [350, 125]

        #self.setFixedSize(self.size_[0], self.size_[1])
        self.setStyleSheet(QSS["BINANCE"])
        self.buttons_needed = []
        AsyncController.window_m(self,"add")

        # ---- set Page -----
        self.items = {}

        # Position buttons manually

        # === Components ===
        self.items["true_v"] = {"user_name":False,"password":False}
        self.items["sub_button"] = QPushButton("Login", self)
        self.items["user_name"] = QLineEdit(self)
        self.items["password"] = QLineEdit(self)

        self.items["password"].setPlaceholderText("Password")
        self.items["user_name"].setPlaceholderText("User name")
        self.items["password"].setEchoMode(QLineEdit.Password)
        
        self.items["Y_first_item"] = 5
        self.items["user_name"].setGeometry(5,self.items["Y_first_item"],self.size_[0]-10,35)
        self.items["password"].setGeometry(5,self.items["Y_first_item"] + 40,self.size_[0]-10,35)
        self.items["sub_button"].setGeometry(5,self.items["Y_first_item"] + 80,self.size_[0]-10,35)

        # =========== Login Button enabling (signals) =========================
        self.items["user_name"].textChanged.connect(lambda x: self.login_texts_slot(x,'user_name'))
        self.items["password"].textChanged.connect(lambda x: self.login_texts_slot(x,'password'))

        # Login and rigister connection ============
        self.items["sub_button"].clicked.connect(lambda: asyncio.create_task(self.login()))

        self.setFixedSize(self.size_[0], self.size_[1])
        self.items["sub_button"].setEnabled(False)

    # ======= Login button enabling (slot) ================
    def login_texts_slot(self,text:str,slot:str):
        self.items["true_v"][slot] = True if text and str(text).strip() and text is not None else False
        self.items["sub_button"].setEnabled(True if all(self.items["true_v"].values()) else False)

    def login_success(self,data):
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


    # On login ========================
    async def login(self):
        self.items["sub_button"].setEnabled(False)
        cipher = CipherUserData()
        un = self.items["user_name"].text()
        pwd = self.items["password"].text()
        data = cipher.get_local_user(pwd,un)
        if data[0] == True:

            accont_info_api = await get_account_info(data[1].get("api-key"),data[1].get("api-secreat"))
            if accont_info_api[0] == False:
                if accont_info_api[1] == "INVALID_API_KEY":
                    pup_message("API Key Error","The saved API Key invalide or has not the correct permitions\nPlease try to reset your user data with correct info\nApi type: HMAC-SHA256\nPermitions neded: Any IP Adress + Read Only",self.ena,"error")
                else:
                    pup_message("API Secreat Error","The saved secreat key is not acceptable with his API Key\nPlease try to reset your user data with correct info",self.ena,"error")
                return
            else:
                pup_message("Seccess",f"You loged in\nClick ok to enter the program",lambda: self.login_success(data[1]),"info")

        elif data[0] == False and data[1] == "incorrect_info":
            pup_message("Incorrect password","User founded but incorrect password or incorrect user encrypt file",self.ena,"warning")
        elif data[0] == False and data[1] == "user_not_found":
            pup_message("User not fond","user not fond in this device",self.ena,"warning")

        
    def ena(self):
        self.items["sub_button"].setEnabled(True)

    # ======== Infrastructure defs ==============
    def closeEvent(self, event):
        self.items["sub_button"].setEnabled(False)
        event.accept()

if __name__ == "__main__":
    import sys
    import qasync
    import core,API


    app = QApplication(sys.argv)
    loop = qasync.QEventLoop()

    async def main():
        for i in core.listeners: asyncio.create_task(i())
        for i in API.listeners: asyncio.create_task(i())
        obj__ = LoggingWidget()
        obj__.show()
        while True:
            await asyncio.sleep(1000)

    try:
        with loop:
            loop.run_until_complete(main())
    except (RuntimeError, KeyboardInterrupt):
        pass