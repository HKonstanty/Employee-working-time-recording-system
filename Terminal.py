import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt


class Terminal:
    BROKER_ADDRESS = "127.0.0.1"
    #BROKER_ADDRESS = "DESKTOP-RA3JCSK"
    TOPIC_LOG = "login/worker"
    TOPIC_CONF = "terminal/configuration"
    PORT = 1883
    #PORT = 8883
    CONFIG_FILE = 'config_file.txt'

    def __init__(self, id):
        self.__ID = id
        self.__client = mqtt.Client(id)
        #self.__client.tls_set("ca.crt")
        self.__client.connect(Terminal.BROKER_ADDRESS, Terminal.PORT)
        self.__name = ""
        self.init_terminal()

    def publish_log(self, msg):
        date = datetime.now()
        dict = {
            "RFID": msg,
            "ID": self.__ID,
            "date": [date.hour, date.minute, date.day, date.month, date.year]
        }
        self.__client.publish(Terminal.TOPIC_LOG, json.dumps(dict))

    def publish_configuration(self, id, name, pin):
        date = datetime.now()
        self.__added_date = date.date()
        self.__name = name
        self.save_conf()
        dict = {
            "_id": id,
            "name": name,
            "pin": pin,
            "date": [date.hour, date.minute, date.day, date.month, date.year]
        }
        self.__client.publish(Terminal.TOPIC_CONF, json.dumps(dict))

    def disconnect(self):
        self.__client.disconnect()

    def save_conf(self):
        with open(Terminal.CONFIG_FILE, 'w') as outfile:
            data = {
                '_id': self.__ID,
                'name': self.__name
            }
            json.dump(data, outfile)

    def reset(self):
        if os.path.exists(Terminal.CONFIG_FILE):
            os.remove(Terminal.CONFIG_FILE)

    @staticmethod
    def config_exist():
        return os.path.exists(Terminal.CONFIG_FILE)

    def init_terminal(self):
        if os.path.exists(Terminal.CONFIG_FILE):
            with open(Terminal.CONFIG_FILE, 'r') as json_file:
                data = json.load(json_file)
                self.__ID = data['_id']
                self.__name = data['name']
                return self

    def get_name(self):
        return self.__name
