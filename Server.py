import random

from Broker import Broker
from DataBaseController import DataBaseController
from TempTerminal import TempTerminal


class Server:

    def __init__(self, controller):
        self.__broker = Broker(self)
        self.__db = DataBaseController()
        self.__tempTerminal = None
        self.__controller = controller

    def new_log(self, logDate):
        RFID = logDate[0]
        date = logDate[1]
        terminalID = logDate[2]
        if self.__db.terminal_exist(terminalID):  # terminal w sytemie
            if self.__db.rfid_exist(RFID):
                status = "Accepted"
                self.__db.worker_log(logDate)
            else:
                status = "Unknown RFID"
        else:  # brak terminala w sytemie
            status = "Unknown terminal"
        self.__db.insert_log(logDate, status)
        self.__controller.insert_new_log(
            "Nowe logowanie, numer terminala {0}, numer karty RFID {1}, status {2}\n".format(terminalID, RFID, status))

    def new_terminal(self, date):
        id = date["_id"]
        name = date["name"]
        pin = date['pin']
        if id == self.__tempTerminal.id and self.__tempTerminal.name == name and self.__tempTerminal.pin == pin:
            data = date['date']
            add_date = '{0}:{1} {2}.{3}.{4}'.format(data[0], data[1], data[2], data[3], data[4])
            del date['pin']
            terminal = {"_id": id, "name": name, "date": add_date}
            self.__db.insert_terminal(terminal)
            mess = "Terminal {0} został dodany pomyślnie\n".format(name)
        elif id != self.__tempTerminal.id or self.__tempTerminal.name != name or self.__tempTerminal.pin != pin:
            mess = "Terminal nie został dadany z powodu różnych danych\n"
        else:
            mess = "Nie udało sie podłączyć terminala z nieznanych przyczyn\n"
        self.__controller.terminal_status(mess)
        self.__controller.insert_new_log(mess)
        self.__broker.unsuscribe()
        self.__tempTerminal = None

    def get_pin(self):
        return self.__tempTerminal.pin

    def create_temp_terminal(self, id, name):
        self.__tempTerminal = TempTerminal()
        self.__tempTerminal.id = id
        self.__tempTerminal.name = name
        self.__tempTerminal.pin = str(random.randint(1000, 9999))

    def subscribe_conf(self):
        self.__broker.subscribe()

    def unsubscribe_conf(self):
        self.__broker.unsuscribe()

    def add_worker(self, worker_dict):
        self.__db.insert_worker(worker_dict)

    def erase_datebase(self):
        self.__db.erase_db()

    def rfid_exist(self, rfid):
        return self.__db.rfid_exist(rfid)

    def get_workers(self):
        return self.__db.get_workers()

    def get_terminals(self):
        return self.__db.get_terminals()

    def update_worker(self, worker_dict):
        self.__db.update_worker(worker_dict)

    def delete_worker(self, worker_id):
        self.__db.delete_worker(worker_id=worker_id)

    def insert_terminal(self, terminal):
        self.__db.insert_terminal(terminal)

    def delete_terminal(self, terminal_id):
        self.__db.delete_terminal(terminal_id=terminal_id)

    def terminal_exist(self, terminal_id):
        return self.__db.terminal_exist(id=terminal_id)

    def get_logs(self):
        return self.__db.get_logs()

    def get_worker(self, id):
        return self.__db.get_worker(id=id)