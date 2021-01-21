import json

import paho.mqtt.client as mqtt


class Broker:
    BROKER_ADDRESS = "127.0.0.1"
    #BROKER_ADDRESS = "DESKTOP-RA3JCSK"
    PORT = 1883
    #PORT = 8883
    TOPIC_LOG = "login/worker"
    TOPIC_CONF = "terminal/configuration"

    def __init__(self, server):
        self.__server = server

        self.__client = mqtt.Client("Server")
        #self.__client.tls_set('ca.crt')
        self.__client.connect(Broker.BROKER_ADDRESS, Broker.PORT)
        self.__client.on_message = self.on_message
        #self.__client.on_connect = self.on_connect
        self.__client.loop_start()
        self.__client.subscribe(Broker.TOPIC_LOG)

    def on_message(self, client, userdata, msg):
        mess = msg.payload.decode("utf-8")  # dict
        date = json.loads(mess)
        if msg.topic == Broker.TOPIC_LOG:
            self.__server.new_log((date["RFID"], date["date"], date["ID"]))
        if msg.topic == Broker.TOPIC_CONF:
            self.__server.new_terminal(date)

    #def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
    #    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    #    client.subscribe("digitest/test1")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

    def disconnect(self):
        self.__client.loop_stop()
        self.__client.disconnect()

    def subscribe(self):
        self.__client.subscribe(Broker.TOPIC_CONF)

    def unsuscribe(self):
        self.__client.unsubscribe(Broker.TOPIC_CONF)
