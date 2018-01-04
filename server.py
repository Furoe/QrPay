# -*- coding: utf-8 -*-
# Author: Furo_Yang

import socket
import threading
import time
import hashlib
import json

class Server():
    def __init__(self):
        self.s_shop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_shop.bind(('127.0.0.1', 45679))
        self.s_shop.listen(10)

        #username and pwd
        self.users = [{'username': 'test1234', 'pwd': 'Abcd@1234'}]

    def listen(self):
        print "[status] listenning"
        while True:
            sock, addr = self.s_shop.accept()
            t = threading.Thread(target=self.shopConn, args=(sock, addr))
            t.start()

    def shopConn(self, sock, addr):
        print "[status] Accept order request from %s:%s"%addr

        data = sock.recv(1024)
        data = json.loads(data)

        print data

        #vertify user
        timestamp = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        userWallet = (self.users[0].get('username') + self.users[0].get('pwd') + timestamp).encode('utf-8')
        self.payStream = hashlib.sha256(userWallet).hexdigest()
        print self.payStream
        if self.payStream == data:
            print "[status] Vertify Pay Success"
        else:
            print "[status] Vertify Pay Fail"

        sock.close()

if __name__ == "__main__":
    server = Server()
    server.listen()