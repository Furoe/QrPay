# -*- coding: utf-8 -*-
# Author: Furo_Yang

import socket
import threading
import time
import hashlib
import json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class Server():
    def __init__(self):
        self.s_shop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_shop.bind(('127.0.0.1', 45679))
        self.s_shop.listen(10)

        #username and pwd
        self.users = [{'userID': 'you', 'username': 'test1234', 'pwd': 'Abcd@1234', 'total': '100'}]
        self.shops = [{'shopID': 'EKSSJHGHGJDHG', 'shopName': 'HappyPay'}]

    def listen(self):
        print "[status] listenning"
        while True:
            sock, addr = self.s_shop.accept()
            t = threading.Thread(target=self.shopConn, args=(sock, addr))
            t.start()

    # Encrypt data
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
        return b2a_hex(ciphertext)

    # Decrypt
    def decrypt(self, key, str):
        length = 16
        count = len(key)
        add = length - (count % length)
        keys = key + ('\0' * add)
        cryptor = AES.new(keys, AES.MODE_CBC, 'This is an IV456')
        plain_text = cryptor.decrypt(a2b_hex(str))
        self.price = plain_text.rstrip('\0')

    def shopConn(self, sock, addr):
        print "[status] Accept order request from %s:%s"%addr

        data = sock.recv(1024)
        data = json.loads(data)

        #vertify shop
        for shop in self.shops:
            shopIDHash = hashlib.sha256(shop.get('shopID')).hexdigest()
            if shopIDHash == data[0:64]:
                self.shopID = shop.get('shopID')
                self.shopName = shop.get('shopName')
            else:
                print 'invalid shopID'

        #vertify price
        self.decrypt(self.shopID, data[64:96])

        # vertify user
        userID = data[99:102]
        for user in self.users:
            if userID == user.get('userID'):
                timestamp = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                #timestamp = time.strftime("%Y-%m-%d %H", time.localtime(time.time()))
                self.userName = user.get('username')
                user.get('total')
                userWallet = (user.get('username') + user.get('pwd') + user.get('total')+ timestamp).encode('utf-8')
                userStream = self.Encrypt(user.get('userID'), userWallet)
                self.userInfo = hashlib.sha256(userStream).hexdigest()
        if self.userInfo == data[102:]:
            print "[status] Vertify Pay Success"
            print "Shop Name: " + self.shopName
            print "Price: " + self.price
            print "Pay From: " + self.userName
        else:
            print "[status] Vertify Pay Fail"

        sock.close()


if __name__ == "__main__":
    server = Server()
    server.listen()