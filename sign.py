import datetime
import json
import os
import random
import sys
import time
from hashlib import md5
import pytz #时区的转换
import requests
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
def getUserAgent(user):
    if user["user-agent"] != 'null':
        return user["user-agent"]

    return random.choice(
        ['Mozilla/5.0 (Android 11 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'])


def parseUserInfo():###获取而用户信息
    allUser = ''
    with open(pwd + "user.json", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            allUser = allUser + line + '\n'

    return json.loads(allUser)
# 工学云加密算法
def encrypt(key, text):
    aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    pad_pkcs7 = pad(text.encode('utf-8'), AES.block_size, style='pkcs7')
    res = aes.encrypt(pad_pkcs7)
    msg = res.hex()
    return msg

def getToken(user):
    url = "https://api.moguding.net:9000/session/user/v3/login"
    t = str(int(time.time() * 1000))
    data = {
        "password": encrypt("23DbtQHR2UMbH6mJ", user["password"]),
        "phone": encrypt("23DbtQHR2UMbH6mJ", user["phone"]),
        "t": encrypt("23DbtQHR2UMbH6mJ", t),
        "loginType": user["type"],
        "uuid": ""
    }
    headers2 = {
        "content-type": "application/json; charset=UTF-8",
        "user-agent": getUserAgent(user)
    }
    res = requests.post(url=url, data=json.dumps(data), headers=headers2)
    return res.json()
def signCheck(user):
    print()
    url = "https://api.moguding.net:9000/attendence/clock/v1/listSynchro"
    token = getToken(user)["data"]["token"]
    header = {
        "accept-encoding": "gzip",
        "content-type": "application/json;charset=UTF-8",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": token,
        "user-agent": getUserAgent(user)
    }
    t = str(int(time.time() * 1000))
    data = {
        "t": encrypt("23DbtQHR2UMbH6mJ", t)
    }
    res = requests.post(url=url, headers=header, data=json.dumps(data))

    lastSignInfo = res.json()["data"][0]
    lastSignDate = lastSignInfo["dateYmd"]
    lastSignType = lastSignInfo["type"]
    hourNow = datetime.datetime.now(pytz.timezone('PRC')).hour
    nowDate = str(datetime.datetime.now(pytz.timezone('PRC')))[0:10]
    #如果lastSignType是END代表当天打上结束
    #如果lastSignType是START打了第一次卡
users = parseUserInfo()#获取用户信息

signCheck(users[0])