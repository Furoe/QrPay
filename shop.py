# -*- coding: utf-8 -*-
# Author:Furo_Yang

import socket
import time
import hashlib
import json
import os
import pyqrcode
import qrtools
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class Shop():
    def __init__(self):
        self.shopName = "Eno"
        self.shopID = "EKSSJHGHGJDHG"
        self.flag = "5ac"

        pass

    #launch a order
    def makeDeal(self):
        price = raw_input("Input price:\n")

        print "Scanning payCode..."
        userInfo = self.scanPayCode()
        check = userInfo[0:3]
        if check == self.flag:
            print "Recognize flag success"
            print userInfo
            orderPrice = self.Encrypt(self.shopID, price)
            shop = hashlib.sha256(self.shopID).hexdigest()
            orderInfo = shop + orderPrice + userInfo
            print orderInfo

            #can't remove flag, if removed ,it's easy to know where the flag is
            self.launchOrder(orderInfo)
        else:
            print userInfo
            print "It's include in the QrCode, I can't ensure wheather it's safe"

    #get pay.png file
    def scanPayCode(self):
        try:
            file = raw_input('> ')
            while not os.path.exists(file):
                print "No payCode"
                file = raw_input('> ')
            print file
            qr = qrtools.QR()
            qr.decode(file)
            return qr.data
        except Exception as msg:
            print msg
            return {}

    def launchOrder(self, payStream):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 45679))
        s.send(json.dumps(payStream).encode())

        result = s.recv(1024)
        print result.decode('utf-8')

    def Encrypt(self, key, str):
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(key)
        add = length - (count % length)
        keys = key + ('\0' * add)
        obj = AES.new(keys, AES.MODE_CBC, 'This is an IV456')
        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        count = len(str)
        add = length - (count % length)
        text = str + ('\0' * add)
        ciphertext = obj.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)

if __name__ == "__main__":
    shop =Shop()
    shop.makeDeal()