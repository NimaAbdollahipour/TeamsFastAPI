import os
from dotenv import load_dotenv, find_dotenv
from des import DES
load_dotenv(find_dotenv())
DES_KEY = os.environ['DES_KEY']
des_obj = DES(DES_KEY)

def enc(string):
    return des_obj.encrypt(string)

def dec(string):
    return des_obj.decrypt(string)

def enc_key(string,key):
    new_des = DES(key)
    return new_des.encrypt(string)