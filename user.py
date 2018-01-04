# -*- coding: utf-8 -*-
# Author:Furo_Yang

import pyqrcode
import qrtools
import time
import base64
import socket
import hashlib
import threading
import json
import rsa

#User
class User():
    def __init__(self):
        self.username = 'test1234'
        self.pwd = 'Abcd@1234'
        self.total = '100'

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
        userWallet = (self.username + self.pwd + self.total + timestamp).encode('utf-8')
        # use AES encrpt userWallet
        self.payStream = hashlib.sha256(userWallet).hexdigest()
        print self.payStream

    # encode Qrcode
    def genQrCode(self):
        self.genPayWallet()
        qrcode = pyqrcode.create(self.payStream)
        qrcode.png("pay.png", scale = 6)

    #decode Qrcode
    def deCode(self, filename):
        qr = qrtools.QR()
        qr.decode(filename)
        print qr.data

    # listen
    def listen(self):
        print "waiting..."

        # establish connect
        sock, addr = self.s.accept()


if __name__ == "__main__":
    use = User()
    use.showPayCode()
