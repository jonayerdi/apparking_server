from channels.generic.websocket import WebsocketConsumer
from .models import ParkingSpot, ParkingSpotState, ParkingCamera
from .views import CAMERAS_ROOT
from django.utils import timezone
from .zybo_bridge.ZyboBridge import ZyboBridge
import threading
import queue
import logging
import json
import os

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
                pass #zyboBridge.messagesOut.put(msg)
            else:
                log.warn('WebSocket receive unknown message type: {}'.format(msg['type']))
        except Exception:
            pass

            
    def disconnect(self, code):
        with parkingSpotSubscriptionsLock:
            for parking in parkingSpotSubscriptions.keys():
                for conn in parkingSpotSubscriptions[parking]:
                    if self == conn:
                        parkingSpotSubscriptions[parking].remove(self)
                        log.info('ParkingConsumer unsubscribe: {}'.format(parking))
        log.info('ParkingConsumer disconnect: {}'.format(code))

# CameraConsumer for camera image updates
class CameraConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        log.info('CameraConsumer connect')

    def receive(self, text_data):
        try:
            log.debug('CameraConsumer receive: {}'.format(text_data))
            msg = json.loads(text_data)
            if msg['type'] == 'CameraSubscribe':
                with cameraSubscriptionsLock:
                    if msg['cameraId'] not in cameraSubscriptions:
                        cameraSubscriptions[msg['cameraId']] = []
                    if self not in cameraSubscriptions[msg['cameraId']]:
                        cameraSubscriptions[msg['cameraId']].append(self)
                        log.info('CameraConsumer subscribe: {}'.format(msg['cameraId']))
            elif msg['type'] == 'CameraUnsubscribe':
                with cameraSubscriptionsLock:
                    if msg['cameraId'] in cameraSubscriptions:
                        if self in cameraSubscriptions[msg['cameraId']]:
                            cameraSubscriptions[msg['cameraId']].remove(self)
                            log.info('CameraConsumer unsubscribe: {}'.format(msg['cameraId']))
            else:
                log.warn('WebSocket receive unknown message type: {}'.format(msg['type']))
        except Exception:
            pass

            
    def disconnect(self, code):
        with cameraSubscriptionsLock:
            for camera in cameraSubscriptions.keys():
                for conn in cameraSubscriptions[camera]:
                    if self == conn:
                        cameraSubscriptions[camera].remove(self)
                        log.info('CameraConsumer unsubscribe: {}'.format(camera))
        log.info('CameraConsumer disconnect: {}'.format(code))

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
                    #Update state
                    parkingSpot = ParkingSpot.objects.filter(parking=msg['parkingId']).filter(number=msg['spotId']).first()
                    newState = ParkingSpotState(parking_spot=parkingSpot
                        , state=ParkingSpotState.STATE_CODES[msg['state']], forced=msg['forced'])
                    newState.save()
                    #Send to Subscribers
                    msg['timestamp'] = str(timezone.now())
                    log.debug('Sending message: {}'.format(json.dumps(msg)))
                    with parkingSpotSubscriptionsLock:
                        if msg['parkingId'] in parkingSpotSubscriptions:
                            for conn in parkingSpotSubscriptions[msg['parkingId']]:
                                conn.send(json.dumps(msg))
                elif msg['type'] == 'ImageUpdate':
                    #Find image folder
                    camera = ParkingCamera.objects.filter(parking=msg['parkingId']).filter(number=msg['cameraId']).first()
                    imageFile = os.path.join(CAMERAS_ROOT, camera.dataFolder, 'image.png')
                    #Write image into file
                    with open(imageFile, 'wb') as fsock:
                        fsock.write(msg['image'])
                    #Send to Subscribers
                    with cameraSubscriptionsLock:
                        if camera.pk in cameraSubscriptions:
                            for conn in cameraSubscriptions[camera.pk]:
                                conn.send(json.dumps({'timestamp': str(timezone.now())}))
                self.messagesQueue.task_done()
            except Exception as e:
                log.error('Exception processing message from ZyboBridge: {}'.format(e))

# Start ZyboBridge server
log = logging.getLogger('ZyboBridge')
log.setLevel(logging.DEBUG)
zyboBridge = ZyboBridge(ip='0.0.0.0', port=6969, logger=log)
zyboBridge.start()

# Start WebSocket notifier
parkingNotifier = ParkingNotifier(zyboBridge.messagesIn)
parkingNotifier.start()
