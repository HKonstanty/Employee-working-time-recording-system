import csv
from datetime import datetime
from Server import Server


class GuiServerController:

    def __init__(self, gui):
        self.__server = Server(self)
        self.__gui = gui

    def add_worker(self, rfid, salary, birthDate, name="", surname="", address="", number="", email="",
                   employedDate=""):
        worker_dict = {
            "_id": -1,
            "RFID": rfid,
            "name": name,
            "surname": surname,
            "address": address,
            "email": email,
            "number": number,
            "birthDate": birthDate,
            "employedDate": employedDate,
            "salary": salary,
            "workTimeTable": []
        }
        self.__server.add_worker(worker_dict)

    def edit_worker(self, id, rfid, salary, birthDate, name, surname, address, number, email, employedDate,
                    timeTable=None):
        worker_dict = {
            "_id": id,
            "RFID": rfid,
            "name": name,
            "surname": surname,
            "address": address,
            "email": email,
            "number": number,
            "birthDate": birthDate,
            "employedDate": employedDate,
            "salary": salary,
            "workTimeTable": timeTable
        }
        self.__server.update_worker(worker_dict)

    def delete_worker(self, worker_id):
        self.__server.delete_worker(worker_id=worker_id)

    def add_terminal(self, terminal_id, name, date):
        terminal = {"_id": terminal_id, "name": name, "date": date}
        self.__server.insert_terminal(terminal)

    def delete_terminal(self, terminal_id):
        self.__server.delete_terminal(terminal_id=terminal_id)

    def terminal_exist(self, terminal_id):
        return self.__server.terminal_exist(terminal_id)

    def rfid_occupied(self, rfid):
        return self.__server.rfid_exist(rfid)

    def get_workers(self):
        workers_list = []
        workers_dict = self.__server.get_workers()
        for worker_dict in workers_dict:
            workers_list.append(worker_dict)
        return workers_list

    def get_terminals(self):
        terminals_list = []
        terminals_dict = self.__server.get_terminals()
        for terminal_dict in terminals_dict:
            terminals_list.append(terminal_dict)
        return terminals_list

    def logs_raport(self, file_name):
        with open(file_name, mode='w', newline='') as csvfile:
            fieldnames = [' ID ', ' terminal ID ', ' RFID ', ' date ', ' status ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()

            logs = self.__server.get_logs()
            log_list = []
            for log in logs:
                log_list.append(log)
            for log_dict in log_list:
                writer.writerow(
                    {' ID ': log_dict["_id"], ' terminal ID ': log_dict["terminalID"], ' RFID ': log_dict["RFID"],
                     ' date ': log_dict["date"], ' status ': log_dict["status"]})

    def terminals_raport(self, file_name):
        with open(file_name, mode='w', newline='') as csvfile:
            fieldnames = [' terminal ID ', ' name ', ' date ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()

            terminals = self.__server.get_terminals()
            term_list = []
            for term in terminals:
                term_list.append(term)
            for term_dict in term_list:
                writer.writerow(
                    {' terminal ID ': term_dict["_id"], ' name ': term_dict["name"],
                     ' date ': term_dict["date"]})

    def count_worked_time(self, timeTable):
        if len(timeTable):
            return 0
        hours = 0
        minutes = 0
        days = 0
        months = 0
        years = 0
        for i, k in zip(timeTable[0::2], timeTable[1::2]):
            hours += (k[0] - i[0])
            minutes += (k[1] - i[1])
            days += (k[2] - i[2])
            months += (k[3] - i[3])
            years += (k[4] - i[4])

        return hours + days * 24 + months * 30.5 * 24 + years * 365 * 12 * 30.5 * 24 + minutes / 60

    def count_time(self, date):
        # date = '12:11 1.01.2020'
        if date == "":
            return "Brak"
        date_time_obj = datetime.strptime(date, '%d/%m/%Y')
        now = datetime.now()
        diff = now - date_time_obj
        # days = diff.days
        years = divmod(diff.total_seconds(), 31536000)[0]

        return years

    def get_workers_list(self):
        workers = self.__server.get_workers()
        work_list = []
        for worker in workers:
            del worker["workTimeTable"]
            work_list.append(worker)
        return work_list

    def get_pin(self):
        return self.__server.get_pin()

    def adding_terminal(self, id, name):
        self.__server.create_temp_terminal(id, name)
        self.__server.subscribe_conf()

    def terminal_status(self, status):
        self.__gui.show_terminal_status(status)

    def insert_new_log(self, log):
        self.__gui.insert_new_log(log)

    def get_worker(self, id):
        return self.__server.get_worker(id)

    def create_raport(self, location, deleted_workers, headers_row, to_deleted):
        location += '.csv'
        workers = self.__server.get_workers()
        work_list = []
        for worker in workers:
            work_list.append(worker)

        for worker in work_list:
            if worker['_id'] in deleted_workers:
                work_list.remove(worker)
        with open(location, mode='w', newline='') as csvfile:
            fieldnames = headers_row
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            for worker in work_list:
                csv_dict = dict([(key, worker[key] if key in worker else None) for key in headers_row])
                if 'age' in headers_row:
                    csv_dict['age'] = self.count_time(worker["birthDate"])
                if 'practice' in headers_row:
                    csv_dict['practice'] = self.count_time(worker["employedDate"])
                workedHours = self.count_worked_time(worker["workTimeTable"])
                if 'workedHours' in headers_row:
                    csv_dict['workedHours'] = workedHours
                if 'reward' in headers_row:
                    csv_dict['reward'] = workedHours * float(worker["salary"])
                writer.writerow(csv_dict)

    def create_work_log(self, path):
        logs = self.__server.get_logs()
        log_list = []
        for log in logs:
            log_list.append(log)

        with open(path, mode='w', newline='') as csvfile:
            fieldnames = [' ID ', ' terminal ID ', ' RFID ', ' date ', ' status ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            for log in log_list:
                writer.writerow(
                    {
                        " ID ": log["_id"],
                        " terminal ID ": log["terminalID"],
                        " RFID ": log["RFID"],
                        " date ": log["date"],
                        " status ": log["status"],
                    }
                )

    def create_terminal_rap(self, path):
        terminals = self.__server.get_terminals()
        term_list = []
        for log in terminals:
            term_list.append(log)

        with open(path, mode='w', newline='') as csvfile:
            fieldnames = [' ID ', ' name ', ' Add date ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            for term in term_list:
                writer.writerow(
                    {
                        " ID ": term["_id"],
                        " name ": term["name"],
                        " Add date ": term["date"],
                    }
                )

    def erase_datebase(self):
        self.__server.erase_datebase()
