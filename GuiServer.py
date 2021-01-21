import json
import os
import threading
from datetime import datetime
from time import sleep
from tkinter import filedialog, messagebox

from tkcalendar import Calendar, DateEntry

from tkinter import *

from GuiServerController import GuiServerController


class Timer(threading.Thread):
    def __init__(self, label, maxValue, gui):
        threading.Thread.__init__(self)
        self.value = maxValue
        self.label = label
        self.stop = threading.Event()
        self.running = True
        self.gui = gui

    def run(self):
        try:
            while self.value > -1 and self.running:
                self.label.config(text=self.value)
                self.value -= 1
                sleep(1)
            self.quit()
            self.gui.show_terminal_status("Nie udało sie dodać temrinala,\nUpłynął czas na wprowadzenie pinu")
        except:
            pass

    def quit(self):
        self.label.config(text="end")

    def stop(self):
        self.running = False


class GuiServer:

    def __init__(self):
        self.__app = GuiServerController(self)
        self.__window = Tk()
        self.__window.title("Server")
        self.__window.bind('<Escape>', lambda event: self.__window.state('normal'))
        self.__window.bind('<F11>', lambda event: self.__window.state('zoomed'))
        # self.__window.protocol("WM_DELETE_WINDOW", self.exit)
        self.init_bar()
        self.__main_frame = Frame(self.__window)
        self.__main_frame.pack(fill=BOTH, expand=TRUE)
        self.init_left_frame()
        self.init_right_frame()
        self.__time_for_add_terminal = 60
        self.__logs_list = []
        self.__window.mainloop()

    def init_bar(self):
        self.__menubar = Menu(self.__window)
        self.__menu = Menu(self.__menubar, tearoff=0)
        self.__menu.add_command(label="Clear database", command=self.clear_datebase)
        self.__menu.add_separator()
        self.__menu.add_command(label="Exit", command=self.__window.quit)
        self.__menubar.add_cascade(label="Menu", menu=self.__menu)

        self.__tools = Menu(self.__menubar, tearoff=0)
        self.__tools.add_command(label="Clear log field", command=self.clear_log)
        self.__tools.add_separator()
        self.__tools.add_command(label="Time for entry pin short", command=lambda: self.set_time(30))
        self.__tools.add_command(label="Time for entry pin medium", command=lambda: self.set_time(60))
        self.__tools.add_command(label="Time for entry pin long", command=lambda: self.set_time(90))
        self.__menubar.add_cascade(label="Tools", menu=self.__tools)

        self.__help = Menu(self.__menubar, tearoff=0)
        self.__menubar.add_cascade(label="Help", menu=self.__help)
        self.__help.add_command(label="About", command=self.show_help)
        self.__help.add_command(label="Information", command=self.show_info)

        self.__window.config(menu=self.__menubar)

    def show_help(self):
        messagebox.showinfo("Informacja", "Aby dodać pracownika należy wejść w zakładkę 'Dodaj pracownika'\n"
                                          "Aby dodać terminal należy wejść w zakładkę 'Dodaj terminal'\n"
                                          "Aby wygenerować raport należy wejść w zakładkę 'Generuj raport' lub 'Generuj inny raport'\n"
                                          "Aby edytować pracowników należy wejść w zakładkę 'Lista pracowników'\n"
                                          "Aby usunąć terminal należy wejść w zakładkę 'Lista terminali'")

    def show_info(self):
        messagebox.showinfo("Informacja", "Nazwa: System Ewidencji Czasu Pracy Pracowników\n"
                                          "Wersja programu: V.2\n"
                                          "Wykonawca: Konstanty Hnat")

    def set_time(self, time):
        self.__time_for_add_terminal = time

    def clear_datebase(self):
        res = messagebox.askyesno("Are you sure?",
                                  "Are you sure you want to permanently delete data from the database?")
        if res:
            self.__app.erase_datebase()

    def init_frame(self):
        self.__main_frame = Frame(self.__window)
        self.__main_frame.pack(padx=10, pady=10)

    def init_left_frame(self):
        self.__left_frame = Frame(self.__main_frame)
        self.__left_frame.pack(side=LEFT)
        add_worker_button = Button(self.__left_frame, text="Dodaj pracownika", width=23, command=self.add_worker_window)
        add_worker_button.pack(padx=10, pady=10)

        workers_list_button = Button(self.__left_frame, text="Lista pracowników", width=23,
                                     command=self.workers_list_window)
        workers_list_button.pack(padx=10, pady=10)

        raport_button = Button(self.__left_frame, text="Generuj raport pracowników", width=23,
                               command=self.raport_window)
        raport_button.pack(padx=10, pady=10)
        add_terminal_button = Button(self.__left_frame, text="Dodaj terminal", width=23,
                                     command=self.add_terminal_window)
        add_terminal_button.pack(padx=10, pady=10)

        terminls_list_button = Button(self.__left_frame, text="Lista terminali", width=23,
                                      command=self.terminals_list_window)
        terminls_list_button.pack(padx=10, pady=10)

        def create_another_raport():
            self.__window.withdraw()
            new_window = Tk()
            new_window.title("Server - create raport")
            lok_label = Label(new_window, text="Lokalizacja raportu", anchor="w", width=15)
            lok_label.grid(row=0, column=0, padx=10, pady=10)
            lok_entry = Entry(new_window, width=25)
            lok_entry.grid(row=0, column=1, padx=10, pady=10)

            def chose_location():
                answer = filedialog.askdirectory()
                lok_entry.delete(0, "end")
                lok_entry.insert(0, answer)

            lok_bt = Button(new_window, text="Wybierz", command=chose_location, width=20)
            lok_bt.grid(row=0, column=2, padx=10, pady=10)

            name_label = Label(new_window, text="Nazwa raportu", anchor="w", width=15)
            name_label.grid(row=1, column=0, padx=10, pady=10)
            name_entry = Entry(new_window, width=25)
            name_entry.grid(row=1, column=1, padx=10, pady=10)

            variable = StringVar(new_window)
            variable.set("Terminali")  # default value

            name_label = Label(new_window, text="Raport:", anchor="w", width=15)
            name_label.grid(row=2, column=0, padx=10, pady=10)
            rap_option = OptionMenu(new_window, variable, "Terminali", "Logów pracowników")
            rap_option.grid(row=2, column=1, padx=10, pady=10)

            def create():
                if self.check_valid(lok_entry.get(), name_entry.get()):
                    path = lok_entry.get() + '/' + name_entry.get() + '.csv'
                    if variable.get() == 'Terminali':
                        self.insert_new_log('Utworzono raport terminali, scieżka {0}\n'.format(path))
                        self.__app.create_terminal_rap(path)
                    if variable.get() == 'Logów pracowników':
                        self.insert_new_log('Utworzono raport logów pracowników, scieżka {0}\n'.format(path))
                        self.__app.create_work_log(path)
                    self.__window.deiconify()
                    new_window.destroy()

            def close():
                self.__window.deiconify()
                new_window.destroy()

            close_bt = Button(new_window, text="Zamknij", width=10, command=close)
            close_bt.grid(row=3, column=0, padx=10, pady=10)
            save_bt = Button(new_window, text="Zapisz", width=10, command=create)
            save_bt.grid(row=3, column=1, padx=10, pady=10)

        log_work_rap_bt = Button(self.__left_frame, text="Generuj inny raport", width=23,
                                 command=create_another_raport)
        log_work_rap_bt.pack(padx=10, pady=10)

    def init_right_frame(self):
        right_frame = Frame(self.__main_frame)
        right_frame.pack(padx=10, pady=10, fill=BOTH, expand=TRUE)

        log_frame = LabelFrame(right_frame, text="Logi")
        log_frame.pack(padx=10, pady=10, fill=BOTH, expand=TRUE)
        self.__resultsfiled = Text(log_frame, state=NORMAL)
        self.__resultsfiled.pack(padx=10, pady=10, fill=BOTH, expand=TRUE)

    def insert_new_log(self, log):
        self.__logs_list.append(log)
        self.__resultsfiled.insert(END, log)

    def clear_log(self):
        self.__logs_list = []
        self.__resultsfiled.delete(1.0, END)

    def add_worker_window(self):
        self.clear_gui()
        self.init_main_frame()
        self.__window.title("Server - add worker")

        left_frame = Frame(self.__main_frame)
        left_frame.pack(side=LEFT, padx=20, pady=20)
        name_label = Label(left_frame, text="Name", width=10, anchor="w")
        name_label.pack(padx=5, pady=5)
        surname_label = Label(left_frame, text="Surname", width=10, anchor="w")
        surname_label.pack(padx=5, pady=5)
        rfid_label = Label(left_frame, text="RFID", width=10, anchor="w")
        rfid_label.pack(padx=5, pady=5)
        address_label = Label(left_frame, text="Address", width=10, anchor="w")
        address_label.pack(padx=5, pady=5)
        email_label = Label(left_frame, text="Email", width=10, anchor="w")
        email_label.pack(padx=5, pady=5)
        number_label = Label(left_frame, text="Number", width=10, anchor="w")
        number_label.pack(padx=5, pady=5)
        salary_label = Label(left_frame, text="Salary", width=10, anchor="w")
        salary_label.pack(padx=5, pady=5)
        birthdate_label = Label(left_frame, text="Birthdate", width=10, anchor="w")
        birthdate_label.pack(padx=5, pady=5)

        name = StringVar()
        surname = StringVar()
        rfid = StringVar()
        address = StringVar()
        email = StringVar()
        number = StringVar()
        salary = StringVar()
        date = StringVar()

        right_frame = Frame(self.__main_frame)
        right_frame.pack(padx=20, pady=20)
        name_entry = Entry(right_frame, width=25, textvariable=name)
        name_entry.pack(padx=5, pady=5)
        surname_entry = Entry(right_frame, width=25, textvariable=surname)
        surname_entry.pack(padx=5, pady=5)

        def rfid_validate(input):
            if self.__app.rfid_occupied(input):
                messagebox.showinfo("Informacja", "Ten numer RFID jest już zajety")
                return False
            else:
                return True

        rfid_reg = self.__window.register(rfid_validate)
        rfid_entry = Entry(right_frame, width=25, textvariable=rfid)
        rfid_entry.pack(padx=5, pady=5)
        rfid_entry.config(validate='focusout', validatecommand=(rfid_reg, '%P'))
        address_entry = Entry(right_frame, width=25, textvariable=address)
        address_entry.pack(padx=5, pady=6)

        def email_validate(input):
            if '@' not in input:
                messagebox.showinfo("Informacja", " Adres email nie jest poprawny")
                return False
            else:
                return True

        email_reg = self.__window.register(email_validate)
        email_entry = Entry(right_frame, width=25, textvariable=email)
        email_entry.pack(padx=5, pady=6)
        email_entry.config(validate='focusout', validatecommand=(email_reg, '%P'))

        def number_validate(input):
            if len(input) != 9 or not input.isdigit():
                messagebox.showinfo("Informacja", "Numer jest niepoprawny")
                return False
            else:
                return True

        def salary_validate(input):
            if input.isdigit():
                return True
            else:
                return False

        reg = self.__window.register(number_validate)
        number_entry = Entry(right_frame, width=25, textvariable=number)
        number_entry.pack(padx=5, pady=6)
        number_entry.config(validate='focusout', validatecommand=(reg, '%P'))
        sal_reg = self.__window.register(salary_validate)
        salary_entry = Entry(right_frame, width=25, textvariable=salary)
        salary_entry.pack(padx=5, pady=6)
        salary_entry.config(validate='key', validatecommand=(sal_reg, '%P'))

        def date_valid(input):
            try:
                date_time_obj = datetime.strptime(input, '%m/%d/%Y')
                now = datetime.now()
                diff = now - date_time_obj
                years = divmod(diff.total_seconds(), 31536000)[0]
                if years > 18:
                    return True
                else:
                    #messagebox.showinfo("Informacja", "Pracownik jest niepełnoletni")
                    return False
            except:
                pass
                #messagebox.showinfo("Informacja", "Data jest nie poprawna")

        birt_reg = self.__window.register(date_valid)
        date_entry = DateEntry(right_frame, width=22, textvariable=date, date_pattern='dd/mm/yyyy')
        date_entry.pack(padx=5, pady=6)
        date = datetime.strptime('01/01/2000', '%d/%m/%Y')
        date_entry.set_date(date)
        #date_entry.config(validate='focusout', validatecommand=(birt_reg, '%P'))

        def add_worker():

            mess = "Wprowadzone dane nie są poprawne\n"
            name = name_entry.get()
            if name == "":
                mess += "Imie nie może być puste\n"
            surname = surname_entry.get()
            if surname == "":
                mess += "Nazwisko nie może być puste\n"
            rfid = rfid_entry.get() if rfid_entry.get() != "" else "Brak"
            email = email_entry.get() if email_entry.get() != "" else "Brak"
            number = number_entry.get() if number_entry.get() != "" else "Brak"
            address = address_entry.get() if address_entry.get() != "" else "Brak"
            salary = salary_entry.get()
            if salary == "":
                mess += "Pensja nie może być pusta\n"

            if date_valid(date_entry.get_date().strftime("%d/%m/%Y")):
                birth = str(date_entry.get_date().strftime("%d/%m/%Y"))
            else:
                mess += "Data jest nie poprawna lub pracownik jest niepełnoletni"
            #else:
            #    mess += "Data jest nieprawidłowa"
            currentDate = str(datetime.today().strftime("%d/%m/%Y"))
            if len(mess) < 35:
                name_entry.delete(0, END)
                surname_entry.delete(0, END)
                rfid_entry.delete(0, END)
                email_entry.delete(0, END)
                number_entry.delete(0, END)
                address_entry.delete(0, END)
                salary_entry.delete(0, END)
                self.__app.add_worker(rfid=rfid, name=name, surname=surname, email=email,
                                      number=number, address=address, salary=salary, birthDate=birth,
                                      employedDate=currentDate)
                self.__logs_list.append("Pomyślnie dodano nowego pracownika\n")
                self.close()
                messagebox.showinfo("Informacja", "Pomyślnie dodano nowego pracownika")
            else:
                messagebox.showinfo("Informacja", mess)

        close_bt = Button(left_frame, text="Close", command=self.close, width=15)
        close_bt.pack(pady=20, padx=20, fill=X, expand=TRUE)
        add_bt = Button(right_frame, text="Save", command=add_worker, width=15)
        add_bt.pack(pady=20, padx=20, fill=X, expand=TRUE)

    def close(self):
        self.clear_gui()
        self.init_main_frame()
        self.init_left_frame()
        self.init_right_frame()
        self.__window.title("Server")
        for log in self.__logs_list:
            self.__resultsfiled.insert(END, log)

    def workers_list_window(self):
        self.clear_gui()
        self.init_main_frame()
        self.__window.title("Server - workers list")
        title = Label(self.__main_frame, text="Workers list", anchor="w")
        title.pack(padx=20, pady=10, fill=X)
        list = Listbox(self.__main_frame, width=200)
        list.pack(padx=20)
        workers = self.__app.get_workers_list()
        for worker in workers:
            list.insert(END, worker)

        def edit():
            selectedWorker = list.get(ANCHOR)
            json_acceptable_string = selectedWorker.replace("'", "\"")
            worker = json.loads(json_acceptable_string)

            self.clear_gui()
            self.init_main_frame()
            self.__window.title("Server - edit worker")

            left_frame = Frame(self.__main_frame)
            left_frame.pack(side=LEFT, padx=20, pady=20)
            name_label = Label(left_frame, text="Name", width=10, anchor="w")
            name_label.pack(padx=5, pady=5)
            surname_label = Label(left_frame, text="Surname", width=10, anchor="w")
            surname_label.pack(padx=5, pady=5)
            rfid_label = Label(left_frame, text="RFID", width=10, anchor="w")
            rfid_label.pack(padx=5, pady=5)
            address_label = Label(left_frame, text="Address", width=10, anchor="w")
            address_label.pack(padx=5, pady=5)
            email_label = Label(left_frame, text="Email", width=10, anchor="w")
            email_label.pack(padx=5, pady=5)
            number_label = Label(left_frame, text="Number", width=10, anchor="w")
            number_label.pack(padx=5, pady=5)
            salary_label = Label(left_frame, text="Salary", width=10, anchor="w")
            salary_label.pack(padx=5, pady=5)
            birthdate_label = Label(left_frame, text="Birthdate", width=10, anchor="w")
            birthdate_label.pack(padx=5, pady=5)

            name = StringVar()
            surname = StringVar()
            rfid = StringVar()
            address = StringVar()
            email = StringVar()
            number = StringVar()
            salary = StringVar()
            date = StringVar()

            right_frame = Frame(self.__main_frame)
            right_frame.pack(padx=20, pady=20)
            name_entry = Entry(right_frame, width=25, textvariable=name)
            name_entry.pack(padx=5, pady=5)
            surname_entry = Entry(right_frame, width=25, textvariable=surname)
            surname_entry.pack(padx=5, pady=5)

            def rfid_validate(input):
                if self.__app.rfid_occupied(input):
                    messagebox.showinfo("Informacja", "Ten numer RFID jest już zajety")
                    return False
                else:
                    return True

            rfid_reg = self.__window.register(rfid_validate)
            rfid_entry = Entry(right_frame, width=25, textvariable=rfid)
            rfid_entry.pack(padx=5, pady=5)
            rfid_entry.config(validate='focusout', validatecommand=(rfid_reg, '%P'))
            address_entry = Entry(right_frame, width=25, textvariable=address)
            address_entry.pack(padx=5, pady=6)

            def email_validate(input):
                if '@' not in input:
                    messagebox.showinfo("Informacja", " Adres email nie jest poprawny")
                    return False
                else:
                    return True

            email_reg = self.__window.register(email_validate)
            email_entry = Entry(right_frame, width=25, textvariable=email)
            email_entry.pack(padx=5, pady=6)
            email_entry.config(validate='focusout', validatecommand=(email_reg, '%P'))

            def number_validate(input):
                if len(input) != 9 or not input.isdigit() or len(input) != 11:
                    return True
                else:
                    return False

            def salary_validate(input):
                if input.isdigit():
                    return True
                else:
                    return False

            reg = self.__window.register(number_validate)
            number_entry = Entry(right_frame, width=25, textvariable=number)
            number_entry.pack(padx=5, pady=6)
            number_entry.config(validate='focusout', validatecommand=(reg, '%P'))

            sal_reg = self.__window.register(salary_validate)
            salary_entry = Entry(right_frame, width=25, textvariable=salary)
            salary_entry.pack(padx=5, pady=6)
            salary_entry.config(validate='key', validatecommand=(sal_reg, '%P'))

            def date_valid(input):
                date_time_obj = datetime.strptime(input, '%m/%d/%y')
                now = datetime.now()
                diff = now - date_time_obj
                years = divmod(diff.total_seconds(), 31536000)[0]
                if years > 18:
                    return True
                else:
                    messagebox.showinfo("Informacja", "Pracownik jest niepełnoletni")
                    return False

            birt_reg = self.__window.register(date_valid)
            date_entry = DateEntry(right_frame, width=22, textvariable=date)
            date_entry.pack(padx=5, pady=6)
            date = datetime.strptime(worker['birthDate'], '%d/%m/%Y')
            date_entry.set_date(date)
            date_entry.config(validate='focusin', validatecommand=(birt_reg, '%P'))

            name_entry.insert(0, worker["name"])
            surname_entry.insert(0, worker["surname"])
            rfid_entry.insert(0, worker["RFID"])
            address_entry.insert(0, worker["address"])
            email_entry.insert(0, worker["email"])
            number_entry.insert(0, worker["number"])
            salary_entry.insert(0, worker['salary'])

            def close():
                self.workers_list_window()

            def save_worker():
                mess = "Wprowadzone dane nie są poprawne\n"
                name = name_entry.get()
                if name == "":
                    mess += "Imie nie może być puste\n"
                surname = surname_entry.get()
                if surname == "":
                    mess += "Nazwisko nie może być puste\n"
                rfid = rfid_entry.get() if rfid_entry.get() != "" else "Brak"
                email = email_entry.get() if email_entry.get() != "" else "Brak"
                number = number_entry.get() if number_entry.get() != "" else "Brak"
                address = address_entry.get() if address_entry.get() != "" else "Brak"
                salary = salary_entry.get()
                if salary == "":
                    mess += "Pensja nie może być pusta\n"
                birth = str(date_entry.get_date().strftime("%d/%m/%Y"))
                if len(mess) < 35:
                    name_entry.delete(0, END)
                    surname_entry.delete(0, END)
                    rfid_entry.delete(0, END)
                    email_entry.delete(0, END)
                    number_entry.delete(0, END)
                    address_entry.delete(0, END)
                    salary_entry.delete(0, END)
                    self.__app.edit_worker(id=worker['_id'], rfid=rfid, name=name, surname=surname, email=email,
                                           number=number, address=address, salary=salary, birthDate=birth,
                                           employedDate=worker["employedDate"])
                    messagebox.showinfo("Informacja", "Pomyślnie zaktualizowano dane pracownika")
                    self.__logs_list.append('Pomyślnie zaktualizowano dane pracownika id {0}\n'.format(worker['_id']))
                    self.workers_list_window()
                else:
                    messagebox.showinfo("Informacja", mess)

            close_bt = Button(left_frame, text="Close", command=close, width=15)
            close_bt.pack(pady=20, padx=20, fill=X, expand=TRUE)
            save_bt = Button(right_frame, text="Save", command=save_worker, width=15)
            save_bt.pack(pady=20, padx=20, fill=X, expand=TRUE)

        def delete():
            selectedWorker = list.get(ANCHOR)
            json_acceptable_string = selectedWorker.replace("'", "\"")
            dict = json.loads(json_acceptable_string)
            list.delete(ANCHOR)
            self.__logs_list.append('Usunięto pracownika, id {0}\n'.format(dict['_id']))
            self.__app.delete_worker(dict["_id"])

        def check_to_edit():
            if list.curselection():
                edit()
            else:
                messagebox.showinfo("Informacja", "Należy wybrać kogoś do edycji")

        def check_to_delete():
            if list.curselection():
                delete()
            else:
                messagebox.showinfo("Informacja", "Należy wybrać kogoś do usunięcia")

        close_bt = Button(self.__main_frame, text="Close", command=self.close, width=15)
        close_bt.pack(pady=20, padx=20, side=LEFT)
        edit_bt = Button(self.__main_frame, text="Edit", command=check_to_edit, width=15)
        edit_bt.pack(pady=20, padx=20, side=LEFT)
        delete_bt = Button(self.__main_frame, text="Delete", command=check_to_delete, width=15)
        delete_bt.pack(pady=20, padx=20, side=LEFT)

    def raport_window(self):
        self.clear_gui()
        self.init_main_frame()
        deleted_workers = []

        top_frame = Frame(self.__main_frame)
        top_frame.pack(fill=X, padx=10, pady=10)
        lok_label = Label(top_frame, text="Lokalizacja raportu", anchor="w")
        lok_label.pack(side=LEFT, padx=5)
        lok_entry = Entry(top_frame, width=25)
        lok_entry.pack(side=LEFT, padx=5)

        def chose_location():
            answer = filedialog.askdirectory(parent=self.__window,
                                             initialdir=os.getcwd())
            lok_entry.delete(0, "end")
            lok_entry.insert(0, answer)

        lok_label.pack(side=LEFT, padx=5)
        lok_bt = Button(top_frame, text="Wybierz", command=chose_location, width=15)
        lok_bt.pack(side=LEFT, padx=5)

        sec_frame = Frame(self.__main_frame)
        sec_frame.pack(fill=X, padx=10, pady=10)
        name_label = Label(sec_frame, text="Nazwa raportu", anchor="w")
        name_label.pack(side=LEFT, padx=5)
        name_entry = Entry(sec_frame, width=25)
        name_entry.pack(side=LEFT, padx=25)

        list_frame = LabelFrame(self.__main_frame, text="Lista pracowników do raportu")
        list_frame.pack(padx=10, pady=10, fill=X, expand="yes")
        list = Listbox(list_frame, width=200)
        list.pack()

        workers = self.__app.get_workers_list()
        for worker in workers:
            list.insert(END, worker)

        def delete_worker():
            if list.curselection():
                selectedWorker = list.get(ANCHOR)
                json_acceptable_string = selectedWorker.replace("'", "\"")
                worker = json.loads(json_acceptable_string)
                deleted_workers.append(worker['_id'])
                list.delete(ANCHOR)
            else:
                messagebox.showinfo("Informacja", "Należy wybrać pracownika do usunięcia")

        def undo():
            size = len(deleted_workers)
            if size == 0:
                messagebox.showinfo("Informacja", "Brak cofnięć")
            else:
                worker = self.__app.get_worker(deleted_workers.pop())
                del worker['workTimeTable']
                list.insert(worker['_id'], worker)

        del_bt = Button(list_frame, text="Usuń", width=15, command=delete_worker)
        del_bt.pack(side=RIGHT, padx=10, pady=10)
        undo_bt = Button(list_frame, text="Cofnij", width=15, command=undo)
        undo_bt.pack(side=RIGHT, padx=10, pady=10)

        checkbt_list = []
        id_var = IntVar()
        id_var.set(1)
        checkbt_list.append(id_var)
        name_var = IntVar()
        checkbt_list.append(name_var)
        surname_var = IntVar()
        checkbt_list.append(surname_var)
        rfid_var = IntVar()
        checkbt_list.append(rfid_var)
        birthDate_var = IntVar()
        checkbt_list.append(birthDate_var)
        age_var = IntVar()
        checkbt_list.append(age_var)
        adr_var = IntVar()
        checkbt_list.append(adr_var)
        email_var = IntVar()
        checkbt_list.append(email_var)
        number_var = IntVar()
        checkbt_list.append(number_var)
        emp_var = IntVar()
        checkbt_list.append(emp_var)
        practice_var = IntVar()
        checkbt_list.append(practice_var)
        salary_var = IntVar()
        checkbt_list.append(salary_var)
        workedH_var = IntVar()
        checkbt_list.append(workedH_var)
        reward_var = IntVar()
        checkbt_list.append(reward_var)

        data_frame = LabelFrame(self.__main_frame, text="Dane do raportu")
        data_frame.pack(padx=10, pady=10, fill=X, expand="yes")

        first_col_frame = Frame(data_frame)
        first_col_frame.pack(side=LEFT)
        id_ckb = Checkbutton(first_col_frame, text="ID", width=20, anchor="w", variable=id_var, onvalue=1, offvalue=0,
                             state=DISABLED)
        id_ckb.pack()
        name_ckb = Checkbutton(first_col_frame, text="Imie", width=20, anchor="w", variable=name_var, onvalue=1,
                               offvalue=0)
        name_ckb.pack()
        surname_ckb = Checkbutton(first_col_frame, text="Nazwisko", width=20, anchor="w", variable=surname_var,
                                  onvalue=1, offvalue=0)
        surname_ckb.pack()

        sec_col_frame = Frame(data_frame)
        sec_col_frame.pack(side=LEFT)
        rfid_ckb = Checkbutton(sec_col_frame, text="RFID", width=20, anchor="w", variable=rfid_var, onvalue=1,
                               offvalue=0)
        rfid_ckb.pack()
        birthDate_ckb = Checkbutton(sec_col_frame, text="Data urodzenia", width=20, anchor="w", variable=birthDate_var,
                                    onvalue=1, offvalue=0)
        birthDate_ckb.pack()
        age_ckb = Checkbutton(sec_col_frame, text="Wiek", width=20, anchor="w", variable=age_var, onvalue=1, offvalue=0)
        age_ckb.pack()

        trd_col_frame = Frame(data_frame)
        trd_col_frame.pack(side=LEFT)
        address_ckb = Checkbutton(trd_col_frame, text="Adres", width=20, anchor="w", variable=adr_var, onvalue=1,
                                  offvalue=0)
        address_ckb.pack()
        number_ckb = Checkbutton(trd_col_frame, text="Numer", width=20, anchor="w", variable=number_var, onvalue=1,
                                 offvalue=0)
        number_ckb.pack()
        email_ckb = Checkbutton(trd_col_frame, text="Email", width=20, anchor="w", variable=email_var, onvalue=1,
                                offvalue=0)
        email_ckb.pack()

        for_col_frame = Frame(data_frame)
        for_col_frame.pack(side=LEFT)
        empDate_ckb = Checkbutton(for_col_frame, text="Data zatrudnienia", width=20, anchor="w", variable=emp_var,
                                  onvalue=1, offvalue=0)
        empDate_ckb.pack()
        practice_ckb = Checkbutton(for_col_frame, text="Staż", width=20, anchor="w", variable=practice_var, onvalue=1,
                                   offvalue=0)
        practice_ckb.pack()
        salary_ckb = Checkbutton(for_col_frame, text="Pensja", width=20, anchor="w", variable=salary_var, onvalue=1,
                                 offvalue=0)
        salary_ckb.pack()

        fiv_col_frame = Frame(data_frame)
        fiv_col_frame.pack(side=LEFT, fill=X)
        workedHours_ckb = Checkbutton(fiv_col_frame, text="Liczba godzin w pracy", width=20, anchor="w",
                                      variable=workedH_var, onvalue=1, offvalue=0)
        workedHours_ckb.pack()
        reward_ckb = Checkbutton(fiv_col_frame, text="Zarobek", width=20, anchor="w", variable=reward_var, onvalue=1,
                                 offvalue=0)
        reward_ckb.pack()

        def create_raport():
            if self.check_valid(lok_entry.get(), name_entry.get()):
                to_delete = []
                headers_row = ['_id']
                if name_var.get() == 0:
                    to_delete.append('name')
                else:
                    headers_row.append('name')
                if surname_var.get() == 0:
                    to_delete.append('surname')
                else:
                    headers_row.append('surname')
                if rfid_var.get() == 0:
                    to_delete.append('RFID')
                else:
                    headers_row.append('RFID')
                if birthDate_var.get() == 0:
                    to_delete.append('birthDate')
                else:
                    headers_row.append('birthDate')
                if age_var.get() == 0:
                    to_delete.append('age')
                else:
                    headers_row.append('age')
                if adr_var.get() == 0:
                    to_delete.append('address')
                else:
                    headers_row.append('address')
                if number_var.get() == 0:
                    to_delete.append('number')
                else:
                    headers_row.append('number')
                if email_var.get() == 0:
                    to_delete.append('email')
                else:
                    headers_row.append('email')
                if emp_var.get() == 0:
                    to_delete.append('employedDate')
                else:
                    headers_row.append('employedDate')
                if practice_var.get() == 0:
                    to_delete.append('practice')
                else:
                    headers_row.append('practice')
                if salary_var.get() == 0:
                    to_delete.append('salary')
                else:
                    headers_row.append('salary')
                if workedH_var.get() == 0:
                    to_delete.append('workedHours')
                else:
                    headers_row.append('workedHours')
                if reward_var.get() == 0:
                    to_delete.append('reward')
                else:
                    headers_row.append('reward')

                location = lok_entry.get() + '/' + name_entry.get()
                self.__logs_list.append('Utworzono raport pracowników, scieżka {0}.csv\n'.format(location))
                self.close()
                self.__app.create_raport(location, deleted_workers, headers_row, to_delete)

        four_frame = Frame(self.__main_frame)
        four_frame.pack(padx=10, pady=10, fill=X, expand="yes")
        gen_bt = Button(four_frame, text="Generuj", width=15, command=create_raport)
        gen_bt.pack(side=RIGHT, padx=10)
        close_bt = Button(four_frame, text="Cofnij", width=15, command=self.close)
        close_bt.pack(side=RIGHT, padx=10)

    def check_valid(self, dir, file):
        mess = "Błędne dane\n"
        if not os.path.isdir(dir):
            mess += "Podany folder nie istnieje\n"
        if os.path.exists(dir + '/' + file+'.csv'):
            mess += "Plik o podanej nazwie już istnieje, dokonaj zmiany, aby kontynuować\n"
        if file == "":
            mess += "Wprowadź nazwę pliku"
        if len(mess) > 15:
            messagebox.showinfo("Informacja", mess)
            return False
        else:
            return True

    def add_terminal_window(self, id="", name=""):
        self.clear_gui()
        self.init_main_frame()
        self.__window.title("Server - add terminal")

        top_frame = Frame(self.__main_frame)
        top_frame.pack(fill=X, padx=10, pady=10, expand=TRUE)
        id_label = Label(top_frame, text="ID terminala", width=20, anchor='w')
        id_label.pack(side=LEFT, pady=10)

        def id_valid(input):
            if self.__app.terminal_exist(input):
                messagebox.showinfo('Informacja', "Termianal o takim id istnieje")
                return False
            else:
                return True

        reg_id = self.__window.register(id_valid)
        id_entry = Entry(top_frame, width=20)
        id_entry.pack(side=LEFT, pady=10)
        id_entry.config(validate='focusout', validatecommand=(reg_id, '%P'))
        if id != "":
            id_entry.insert(0, id)

        mid_frame = Frame(self.__main_frame)
        mid_frame.pack(fill=X, padx=10, pady=10, expand=TRUE)
        name_label = Label(mid_frame, text="Nazwa terminala", width=20, anchor='w')
        name_label.pack(side=LEFT, pady=10)
        name_entry = Entry(mid_frame, width=20)
        name_entry.pack(side=LEFT, pady=10)
        if name != "":
            name_entry.insert(0, name)

        def is_valid():
            mess = ""
            if self.__app.terminal_exist(id_entry.get()):
                mess += 'Terminal o takim id już istnieje'
            if id_entry.get() == "":
                mess += 'Brak id terminala'
            if name_entry.get() == "":
                mess += "Nazwa jest za krótka"
            if len(mess) > 0:
                messagebox.showinfo('Informacja', mess)
            else:
                next()

        def next():
            id = id_entry.get()
            name = name_entry.get()
            self.clear_gui()
            self.init_main_frame()

            top_frame = Frame(self.__main_frame)
            top_frame.pack(fill=X, padx=10, pady=10, expand=TRUE)
            id_label = Label(top_frame, text="ID terminala: {0}".format(id), width=30, anchor='w')
            id_label.pack(side=LEFT, pady=10)

            mid_frame = Frame(self.__main_frame)
            mid_frame.pack(fill=X, padx=10, pady=10, expand=TRUE)
            name_label = Label(mid_frame, text="Nazwa terminala: {0}".format(name), width=20, anchor='w')
            name_label.pack(side=LEFT, pady=10)

            third_frame = Frame(self.__main_frame)
            third_frame.pack(fill=X, padx=10, pady=10, expand=TRUE)
            self.__app.adding_terminal(id, name)
            pin = self.__app.get_pin()

            pin_label = Label(third_frame, text="Prosze wprowadzić podany pin na terminalu w celu połączenia")
            pin_label.pack(pady=10)
            pin_l = Label(third_frame, text=pin)
            pin_l.pack(pady=10)

            bottom_frame = Frame(self.__main_frame)
            bottom_frame.pack(fill=X, padx=10, pady=10)
            time_frame = LabelFrame(bottom_frame, text="Czas pozostały na wprowdzenie pinu")
            time_frame.pack(padx=10, pady=10, fill=X, expand="yes")
            time_counter = Label(time_frame, text="start")
            time_counter.pack(padx=10, pady=10)
            self.__timer = Timer(time_counter, self.__time_for_add_terminal, self)
            self.__timer.start()

            back_bt = Button(bottom_frame, text="Back", width=10,
                             command=lambda: self.add_terminal_window(id=id, name=name))
            back_bt.pack(pady=10, padx=10)

        bottom_frame = Frame(self.__main_frame)
        bottom_frame.pack(fill=X, padx=10, pady=10)
        close_bt = Button(bottom_frame, text="Close", width=10, command=self.close)
        close_bt.pack(side=LEFT, pady=10, padx=10)
        next_bt = Button(bottom_frame, text="Next", width=10, command=is_valid)
        next_bt.pack(side=RIGHT, pady=10, padx=10)

    def show_terminal_status(self, status):
        self.close()
        messagebox.showinfo("Informacja", status)

    def terminals_list_window(self):
        self.clear_gui()
        self.init_main_frame()
        self.__window.title("Server - terminals list")
        title = Label(self.__main_frame, text="Terminals list", anchor="w")
        title.pack(padx=20, pady=10, fill=X)
        list = Listbox(self.__main_frame, width=150)
        list.pack(padx=20)

        terminals = self.__app.get_terminals()
        for terminal in terminals:
            list.insert(END, terminal)

        def delete():
            if list.curselection():
                selectedTerminal = list.get(ANCHOR)
                json_acceptable_string = selectedTerminal.replace("'", "\"")
                dict = json.loads(json_acceptable_string)
                list.delete(ANCHOR)
                self.__logs_list.append("Usunięto termianal id: {0}\n".format(dict['_id']))
                self.__app.delete_terminal(dict["_id"])
            else:
                messagebox.showinfo("Informacja", "Należy wybrać coś do usunięcia")

        close_bt = Button(self.__main_frame, text="Close", command=self.close, width=15)
        close_bt.pack(pady=20, padx=20, side=LEFT)
        delete_bt = Button(self.__main_frame, text="Delete", command=delete, width=15)
        delete_bt.pack(pady=20, padx=20, side=LEFT)

    def clear_gui(self):
        self.__main_frame.destroy()

    def init_main_frame(self):
        self.__main_frame = Frame(self.__window)
        self.__main_frame.pack(fill=BOTH, expand=TRUE)


if __name__ == "__main__":
    gui = GuiServer()
