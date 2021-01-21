from pymongo import MongoClient


class DataBaseController:

    def __init__(self):
        self.__cluster = MongoClient(
            "mongodb+srv://admin:admin@sem-5.qsnxz.mongodb.net/admin?retryWrites=true&w=majority")
        self.__db = self.__cluster["Server"]
        self.__workers = self.__db["Workers"]
        self.__logs = self.__db["Logs"]
        self.__terminals = self.__db["Terminals"]

    def insert_worker(self, worker):
        id = self.__workers.count_documents({})
        while self.__workers.count_documents({'_id': id}) > 0:
            id += 1
        worker["_id"] = id
        self.__workers.insert_one(worker)

    def insert_log(self, logDate, status):
        id = self.__logs.count_documents({})
        terminal_id = logDate[2]
        rfid = logDate[0]
        date = '{0}:{1} {2}.{3}.{4}'.format(logDate[1][0], logDate[1][1], logDate[1][2], logDate[1][3], logDate[1][4])
        log = {"_id": id, "terminalID": terminal_id, "RFID": rfid, "date": date, "status": status}
        self.__logs.insert_one(log)

    def insert_terminal(self, terminal):
        self.__terminals.insert_one(terminal)

    def update_rfid(self, worker, new_rfid):
        self.__workers.update_one({"_id": worker["_id"]}, {"$set": {"RFID": new_rfid}})

    def update_worker(self, worker):
        old_worker = self.__workers.find_one({"_id": worker["_id"]})
        worker["workTimeTable"] = old_worker["workTimeTable"]
        self.__workers.delete_one({"_id": worker["_id"]})
        self.__workers.insert_one(worker)

    def delete_worker(self, worker=None, worker_id=None):
        self.__workers.delete_one({"_id": worker_id})

    def delete_terminal(self, terminal=None, terminal_id=None):
        self.__terminals.delete_one({"_id": terminal_id})

    def worker_log(self, logDate):
        RFID = logDate[0]
        date = logDate[1]
        terminalID = logDate[2]
        worker = self.__workers.find({"RFID": RFID})
        worker_dict = []
        for item in worker:
            worker_dict.append(item)
        worker_dict[0]['workTimeTable'].append(date)
        self.__workers.update_one({"RFID": RFID}, {"$set": {"workTimeTable": worker_dict[0]['workTimeTable']}})

    def rfid_exist(self, RFID):
        return self.__workers.count_documents({"RFID": RFID}) > 0

    def terminal_exist(self, id):
        return self.__terminals.count_documents({"_id": id}) > 0

    def get_workers(self):
        return self.__workers.find({})

    def get_terminals(self):
        return self.__terminals.find({})

    def get_logs(self):
        return self.__logs.find({})

    def get_worker(self, id):
        return self.__workers.find_one({"_id": id})

    def erase_db(self):
        self.__workers.drop()
        self.__terminals.drop()
        self.__logs.drop()
