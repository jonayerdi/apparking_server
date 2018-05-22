from channels.generic.websocket import WebsocketConsumer
from .ZyboBridge import ZyboBridge
import threading
import queue
import logging
import json

# ZyboBridge server
log = logging.getLogger('ZyboBridge')
zyboBridge = ZyboBridge(ip='127.0.0.1', port=6969, logger=log)
zyboBridge.start()

# Consumers notifier
parkingNotifier = ParkingNotifier(zyboBridge.messagesIn)
parkingNotifier.start()

class ParkingNotifier(threading.Thread):
    def __init__(self, messagesQueue):
        super().__init__()
        self.consumers = {}
        self.messagesQueue = messagesQueue

    def run(self):
        while(True):
            msg = self.messagesQueue.get()
            #Do stuff
            self.messagesQueue.task_done()

class ParkingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        log.info('WebSocket connect')

    def receive(self, text_data):
        log.info('WebSocket receive: {}'.format(text_data))

    def disconnect(self, code):
        log.info('WebSocket disconnect: {}'.format(code))
