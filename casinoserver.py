from socket import *
import sqlite3
import sys
import multiprocessing


# класс работающий с клиентским сокетом
class manager:
    def __init__(self, client):
        self.con = sqlite3.connect("casinodatabase.db")
        self.cur = self.con.cursor()
        self.client = client

    # получить имя профиля по id
    def getusername(self, id):
        self.client.send(bytes(str(self.cur.execute(f"""SELECT username
                                        FROM profiletable WHERE id = {id}""").fetchall()[0][0]), 'utf-8'))
    # обработка регистрации
    def registration(self, login, password):
        self.cur.execute(
            f"""INSERT INTO profiletable(chips, username, password) VALUES(1000, \"{login}\", \"{password}\")""")
        self.con.commit()

    # получить кол-во фишек на аккаунте
    def getchips(self, id):
        self.client.send(bytes(str(self.cur.execute(f"""SELECT chips
                                        FROM profiletable WHERE id = {id}""").fetchall()[0][0]), 'utf-8'))

    # установить заданное кол-во фишек на аккаунте
    def setchips(self, id, chips):
        self.cur.execute(
            f"""UPDATE profiletable
                    SET chips = \"{chips}\"
                    WHERE id = {id}""")
        self.con.commit()

    def entertogame(self, id, game):
        pass
    # тут что-то будет

    def getprofile(self, id):
        self.client.send(bytes('|'.join(list(map(str, self.cur.execute(f"""SELECT chips, username, password
                                                FROM profiletable WHERE id = {id}""").fetchall()[0]))), 'utf-8'))

    # функция ищет профиль по логину паролю и номеру (реализуется при входе в аккаунт)
    def getid(self, login, password):
        buff = self.cur.execute(f"""SELECT id
                                                FROM profiletable WHERE password = \"{password}\" and username = \"{login}\"""").fetchall()
        if len(buff) == 0:
            self.client.send(b'empty')
        else:
            self.client.send(bytes(str(buff[0][0]), 'utf-8'))

    # обработка запроса установки логина
    def setlogin(self, id, login):
        self.cur.execute(
            f"""UPDATE profiletable
                    SET username = \"{login}\"
                    WHERE id = {id}""")
        self.con.commit()

    # обработка запроса установки пароля
    def setpassword(self, id, password):
        self.cur.execute(
            f"""UPDATE profiletable
                    SET password = \"{password}\"
                    WHERE id = {id}""")
        self.con.commit()

    def addchips(self, id, chips):
        self.cur.execute(
            f"""UPDATE profiletable
                    SET chips = chips + \"{chips}\"
                    WHERE id = {id}""")
        self.con.commit()

    def getstatus(self, id, window):
        pass

    # Функция для внутреннего применения классом manager

    def getlogin(self, id):
        return str(self.cur.execute(f"""SELECT username
                                           FROM profiletable WHERE id = {id}""").fetchall()[0][0])

    # Функция действий для покера
    def currpokerevent(self, id, event):
        pass

    def currblackjackevent(self, id, event):
        pass

    def sendcards(self, id, currentgame, cards):
        if currentgame == 'poker':
            pass
        elif currentgame == 'blackjack':
            pass


def activeserver(client, address, server):
    ex = manager(client)
    while True:
        while True:
            try:
                data = client.recv(1024)
                if len(data.decode("utf-8")) > 0:
                    data = data.decode("utf-8")
                    if len(data.split('|')) != 0:
                        command, context = data.split('|')[0], data.split('|')[1:]
                        if command == 'getusername':
                            ex.getusername(context[0])
                        if command == 'registration':
                            ex.registration(context[0], context[1])
                        if command == 'getchips':
                            ex.getchips(context[0])
                        if command == 'setchips':
                            ex.setchips(context[0], context[1])
                        if command == 'entertogame':
                            ex.entertogame(context[0], context[1])
                        if command == 'getprofile':
                            ex.getprofile(context[0])
                        if command == 'getid':
                            ex.getid(context[0], context[1])
                        if command == 'setlogin':
                            ex.setlogin(context[0], context[1])
                        if command == 'setpassword':
                            ex.setpassword(context[0], context[1])
                        if command == 'getstatus':
                            ex.getstatus(context[0], context[1])
                        if command == 'addchips':
                            ex.addchips(context[0], context[1])
                        if command == 'currpokerevent':
                            ex.currpokerevent(context[0], context[1])
                        if command == 'currblackjackevent':
                            ex.currblackjackevent(context[0], context[1])
                        if command == 'sendcards':
                            ex.sendcards(command[0], context[1], command[2:])


                else:
                    client, address = server.accept()
            except:
                break


if __name__ == "__main__":
    hostName = gethostbyname_ex(gethostname())[-1][-1]
    with socket(AF_INET, SOCK_STREAM) as server:
        server.bind((hostName, 5666))
        print(hostName)
        server.listen(1)
        while True:
            client, addr = server.accept()
            p = multiprocessing.Process(target=activeserver, args=(client, addr, server))
            p.start()
