# -*- coding: utf-8 -*-
# Author:Furo_Yang

import socket
import time
import hashlib
import json
import os
import pyqrcode
import qrtools

class Shop():
    def __init__(self):
        self.shopName = "Eno"
        self.shopID = "EKSSJHGHGJDHG"

        pass

    #launch a order
    def launchOrder(self):
        price = raw_input("Input price:\n")

        print "Scanning payCode..."
        userInfo = self.scanPayCode()
        print userInfo

        self.userConfirm(userInfo)



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

    def userConfirm(self, payStream):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 45679))
        s.send(json.dumps(payStream).encode())

        result = s.recv(1024)
        print result.decode('utf-8')

if __name__ == "__main__":
    shop =Shop()
    shop.launchOrder()