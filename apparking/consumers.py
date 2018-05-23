from channels.generic.websocket import WebsocketConsumer
from .zybo_bridge.ZyboBridge import ZyboBridge
import threading
import queue
import logging
import json

# Global ParkingConsumer subscriptions
parkingSpotSubscriptions = {}
parkingSpotSubscriptionsLock = threading.Lock()

# Global CameraConsumer subscriptions
cameraSubscriptions = {}
cameraSubscriptionsLock = threading.Lock()

# ParkingConsumer for parking state updates
class ParkingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        log.info('ParkingConsumer connect')

    def receive(self, text_data):
        try:
            log.debug('ParkingConsumer receive: {}'.format(text_data))
            msg = json.loads(text_data)
            if msg['type'] == 'ParkingSubscribe':
                with parkingSpotSubscriptionsLock:
                    if msg['parkingId'] not in parkingSpotSubscriptions:
                        parkingSpotSubscriptions[msg['parkingId']] = []
                    if self not in parkingSpotSubscriptions[msg['parkingId']]:
                        parkingSpotSubscriptions[msg['parkingId']].append(self)
                        log.info('ParkingConsumer subscribe: {}'.format(msg['parkingId']))
            elif msg['type'] == 'ParkingUnsubscribe':
                with parkingSpotSubscriptionsLock:
                    if msg['parkingId'] in parkingSpotSubscriptions:
                        if self in parkingSpotSubscriptions[msg['parkingId']]:
                            parkingSpotSubscriptions[msg['parkingId']].remove(self)
                            log.info('ParkingConsumer unsubscribe: {}'.format(msg['parkingId']))
            elif msg['type'] == 'ParkingSpotUpdate':
                zyboBridge.messagesOut.put(msg)
            else:
                log.warn('WebSocket receive unknown message type: {}'.format(msg['type']))
        except Exception:
            pass
            
    def disconnect(self, code):
        log.info('ParkingConsumer disconnect: {}'.format(code))

# WebSocket notifier class
class ParkingNotifier(threading.Thread):
    def __init__(self, messagesQueue):
        super().__init__()
        self.messagesQueue = messagesQueue

    def run(self):
        while(True):
            try:
                msg = self.messagesQueue.get()
                if msg['type'] == 'ParkingSpotUpdate':
                    with parkingSpotSubscriptionsLock:
                        if msg['parkingId'] in parkingSpotSubscriptions:
                            for conn in parkingSpotSubscriptions[msg['parkingId']]:
                                conn.send(msg)
                elif msg['type'] == 'ImageUpdate':
                    pass #TODO
                self.messagesQueue.task_done()
            except Exception as e:
                log.error('Exception processing message from ZyboBridge: {}'.format(e))

# Start ZyboBridge server
log = logging.getLogger('ZyboBridge')
zyboBridge = ZyboBridge(ip='127.0.0.1', port=6969, logger=log)
zyboBridge.start()

# Start WebSocket notifier
parkingNotifier = ParkingNotifier(zyboBridge.messagesIn)
parkingNotifier.start()
