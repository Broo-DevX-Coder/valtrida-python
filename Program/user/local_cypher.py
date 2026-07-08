import os

import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
from Crypto.Hash import SHA256

from base.files_folders import USERS_FILE

class CipherUserData():
    def __init__(self):
        self.AES_MODE = AES.MODE_GCM

    def new_register_ciphering(self,password:str,data:dict):
        try:
            salt = get_random_bytes(16)
            password_key = PBKDF2(password,salt,dkLen=32, count=200000, hmac_hash_module=SHA256)
            
            data = base64.b64encode(json.dumps(data).encode())

            cipher = AES.new(password_key,self.AES_MODE)
            ciphertext,tag = cipher.encrypt_and_digest(data)
            return salt+cipher.nonce+tag+ciphertext
        
        except Exception as e:
                return False
    
    def decrypt_register_data(self,password:str,token:bytes):
        try:
            salt = token[:16]
            nonce = token[16:32]
            tag = token[32:48]
            ciphertext = token[48:]

            password_key = PBKDF2(password,salt,dkLen=32, count=200000, hmac_hash_module=SHA256)
            cipher = AES.new(password_key,self.AES_MODE,nonce=nonce)
            data = base64.b64decode(cipher.decrypt_and_verify(ciphertext,tag).decode()).decode()
            return json.loads(data)
            
        except ValueError:
            return False

    def save_new_local_user(self,password:str,data:dict):
        user_file = os.path.join(USERS_FILE,f"{data.get('user_name')}.enc")
        if not os.path.exists(user_file):
            token = self.new_register_ciphering(password,data)

            with open(user_file,"wb") as f:
                f.write(token)

            return True
        else:
            return False
        

    def get_local_user(self,password:str,un:str):
        user_file = os.path.join(USERS_FILE,f"{un}.enc")
        if os.path.exists(user_file):
            with open(user_file,"rb") as f:
                token = f.read()
            data = self.decrypt_register_data(password,token)
            if data != False:
                return True,data
            else: 
                return False,"incorrect_info"
        else:
            return False,"user_not_found"