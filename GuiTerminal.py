from tkinter import *
from tkinter import messagebox

from GuiTerminalController import GuiTerminalController


class GuiTerminal:

    def __init__(self):
        self.__app = GuiTerminalController()
        self.__window = Tk()
        self.__window.title("Terminal")
        self.init_main_frame()
        if self.__app.config_exist():
            self.init_second_window()
        else:
            self.init_first_window()
        self.__window.mainloop()

    def init_first_window(self):
        id_label = Label(self.__main_frame, text="Podaj ID terminala:", width=20, anchor="w")
        id_label.grid(row=0, column=0, pady=10, padx=15)
        self.__id_entry = Entry(self.__main_frame, width=25)
        self.__id_entry.grid(row=0, column=1, pady=10, padx=15)

        name_label = Label(self.__main_frame, text="Podaj nazwe terminala:", width=20, anchor="w")
        name_label.grid(row=1, column=0, pady=10, padx=15)
        self.__name_entry = Entry(self.__main_frame, width=25)
        self.__name_entry.grid(row=1, column=1, pady=10, padx=15)

        pin_label = Label(self.__main_frame, text="Podaj pin:", width=20, anchor="w")
        pin_label.grid(row=2, column=0, pady=10, padx=15)
        self.__pin_entry = Entry(self.__main_frame, width=25)
        self.__pin_entry.grid(row=2, column=1, pady=10, padx=15)

        save_button = Button(self.__main_frame, text="Zapisz", width=15, command=self.add_terminal)
        save_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def add_terminal(self):
        mess = "Wprowadzone dane są niepoprawne\n"
        if self.__id_entry.get() == "":
            mess += "Wprowadz id\n"
        if self.__name_entry.get() == "":
            mess += "Wprowadz nazwe\n"
        if self.__pin_entry.get() == "":
            mess += "Wprowadz pin"
        if len(mess) > 35:
            messagebox.showinfo('Informacja', mess)
        else:
            self.save()

    def save(self):
        self.__window.title("Terminal " + str(self.__name_entry.get()))
        self.__app.send_conf(self.__id_entry.get(), self.__name_entry.get(), self.__pin_entry.get())
        self.__main_frame.destroy()
        self.init_main_frame()
        self.init_second_window()

    def init_second_window(self):
        rfid_label = Label(self.__main_frame, text="Podaj numer RFID:", width=20, anchor="w")
        rfid_label.grid(row=0, column=0, pady=10, padx=15)
        self.__rfid_entry = Entry(self.__main_frame, width=25)
        self.__rfid_entry.grid(row=0, column=1, pady=10, padx=15)

        save_button = Button(self.__main_frame, text="Wyślij", width=15, command=self.send)
        save_button.grid(row=2, column=1, padx=10, pady=10)

        reset_button = Button(self.__main_frame, text="Reset", width=15, command=self.restart_gui)
        reset_button.grid(row=2, column=2, padx=10, pady=10)

    def send(self):
        self.__app.new_log(self.__rfid_entry.get())
        self.__window.title("Terminal " + str(self.__app.get_terminal_name()))

    def init_main_frame(self):
        self.__main_frame = Frame(self.__window)
        self.__main_frame.pack()

    def restart_gui(self):
        self.__app.reset_terminal()
        self.__main_frame.destroy()
        self.__main_frame = Frame(self.__window)
        self.__window.title("Terminal")
        self.__main_frame.pack()
        self.init_first_window()


if __name__ == "__main__":
    gui = GuiTerminal()
