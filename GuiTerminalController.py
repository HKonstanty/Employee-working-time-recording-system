from datetime import datetime

from DataBaseController import DataBaseController
from Terminal import Terminal


class GuiTerminalController:

    def __init__(self):
        self.__terminal = None

    #def add_terminal(self, terminal_id, name):
    #    self.__terminal = Terminal(terminal_id)
     #   # datetime object containing current date and time
     #   now = datetime.now()
     #   # dd/mm/YY H:M:S
     #   dt_string = now.strftime("%H:%M %d/%m/%Y")
     #   print("date and time =", dt_string)

    def new_log(self, rfid):
        if self.__terminal is None:
            self.__terminal = Terminal("-1")
            self.__terminal.init_terminal()
        self.__terminal.publish_log(rfid)

    def send_conf(self, id, name, pin):
        self.__terminal = Terminal(id)
        self.__terminal.publish_configuration(id, name, pin)

    def reset_terminal(self):
        if self.__terminal is None:
            self.__terminal = Terminal("-1")
        self.__terminal.reset()
        self.__terminal = None

    def config_exist(self):
        return Terminal.config_exist()

    def get_terminal_name(self):
        return self.__terminal.get_name()
