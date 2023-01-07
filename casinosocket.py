from socket import *
import sqlite3
import sys

'''Функции в socketprocessor выполняют ровно то, что написано в их названии.
-------------------------------------
Первое слово либо get либо set
get - информация отправляется, потом принимается
set - информация отправляется на сервер, на нём и обрабатывается, ничего не принимается
исключения:
addgroup - создание группы
ext - прервать соединение с сервером
registration - создание нового аккаунта с объявленными логином, паролем и номером
idfromnumber - получить персональный айди-номер из номера (телефона) профиля
--------------------------------------
второе слово - ключ, т.е. name|login|password|id|ids|text|profile|ipaddress соответственно то, что мы должны получить 
или отправить
'''


class socketprocessor:
    def __init__(self, ip):
        print(ip)
        hostName = gethostbyname(ip.strip())
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((hostName, 5666))

    def getusername(self, id):
        self.client.send(bytes(f"getusername|{id}", "utf-8"))
        return self.client.recv(2048)

    def registration(self, login, password):
        self.client.send(bytes(f"registration|{login}|{password}", "utf-8"))

    def getchips(self, id):
        self.client.send(bytes(f"getchips|{id}", "utf-8"))
        return self.client.recv(2048)

    def setchips(self, id, value):
        self.client.send(bytes(f"setchips|{id}|{value}", "utf-8"))

    def entertogame(self, id, game):
        self.client.send(bytes(f"entertogame|{id}|{game}", "utf-8"))
        return self.client.recv(2048)

    def ext(self):
        self.client.close()

    def getprofile(self, id):
        self.client.send(bytes(f"getprofile|{id}", "utf-8"))
        return self.client.recv(2048)

    def getid(self, login, password):
        print(login, password)
        self.client.send(bytes(f"getid|{login}|{password}", "utf-8"))
        return self.client.recv(2048)

    def setlogin(self, id, login):
        self.client.send(bytes(f"setlogin|{id}|{login}", "utf-8"))

    def setpassword(self, id, password):
        self.client.send(bytes(f"setpassword|{id}|{password}", "utf-8"))

    def getstatus(self, id, window):
        self.client.send(bytes(f"getstatus|{id}|{window}", "utf-8"))
        return self.client.recv(2048)

    def addchips(self, id, chips):
        self.client.send(bytes(f"addchips|{id}|{chips}", "utf-8"))

    def currpokerevent(self, id, event):
        self.client.send(bytes(f"currpokerevent|{id}|{event}", "utf-8"))

    def currblackjackevent(self, id, event):
        self.client.send(bytes(f"currblackjackevent|{id}|{event}", "utf-8"))

    def sendcards(self, id, currentgame, cards):
        self.client.send(bytes(f"sendcards|{id}|{currentgame}|{'|'.join(cards)}", "utf-8"))
