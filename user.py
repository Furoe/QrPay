# -*- coding: utf-8 -*-
# Author:Furo_Yang

import pyqrcode
import qrtools
import time
import socket
import hashlib
import threading
import json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

#User
class User():
    def __init__(self):
        self.username = 'test1234'
        self.pwd = 'Abcd@1234'
        self.total = '100'
        self.flag = '5ac'
        self.userID = 'you'

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 45678))


    # define pay process
    def showPayCode(self):
        try:
            while True:
                print '-'*40
                ans = raw_input('Show your payCode ?(yes/no)\n')
                if ans == "yes" or ans == "y":
                    t = threading.Thread(target=self.genQrCode)
                    t.start()
                    print "PayCode is available in 1 minute"
                    # listen to server
                    #self.listen()
                elif ans == 'no' or ans == 'n':
                    print "Cancle to genereate your PayCode"
                else:
                    print "Error Input"
        except Exception as msg:
            print msg


    # create PayWallet
    def genPayWallet(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
        #timestamp = time.strftime("%Y-%m-%d %H", time.localtime(time.time()))
        userWallet = (self.username + self.pwd + self.total + timestamp).encode('utf-8')
        # use AES encrpt userWallet
        userStream = self.Encrypt(userWallet)
        userInfo = hashlib.sha256(userStream).hexdigest()
        self.payStream = self.flag + self.userID + userInfo

    # encode Qrcode
    def genQrCode(self):
        self.genPayWallet()
        qrcode = pyqrcode.create(self.payStream)
        qrcode.png("pay.png", scale = 6)

    #decode Qrcode
    def deCode(self, filename):
        qr = qrtools.QR()
        qr.decode(filename)

     # Encrypt data
    def Encrypt(self, str):
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(self.userID)
        add = length - (count % length)
        keys = self.userID + ('\0'*add)
        obj = AES.new(keys, AES.MODE_CBC, 'This is an IV456')
        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        count = len(str)
        add = length - (count % length)
        text = str + ('\0' * add)
        ciphertext = obj.encrypt(text)
        return b2a_hex(ciphertext)

    # listen
    def listen(self):
        print "waiting..."

        # establish connect
        sock, addr = self.s.accept()


if __name__ == "__main__":
    use = User()
    use.showPayCode()
