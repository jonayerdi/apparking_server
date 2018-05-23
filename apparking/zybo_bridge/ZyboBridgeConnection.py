#!/usr/bin/python

import threading
import socket

from . import ZyboBridgeConstants

class ZyboBridgeConnection(threading.Thread):

    def __init__(self, server, sock, address):
        super().__init__()
        self.logger = server.logger
        self.server = server
        self.sock = sock
        self.address = address
        self.parkingId = None
        self.messageHandlers = {
            ZyboBridgeConstants.MESSAGE_TYPES_IN['ServerIdRequest']: self.handleServerIdRequest,
            ZyboBridgeConstants.MESSAGE_TYPES_IN['ParkingIdUpdate']: self.handleParkingIdUpdate,
            ZyboBridgeConstants.MESSAGE_TYPES_IN['ParkingSpotUpdate']: self.handleParkingSpotUpdate,
            ZyboBridgeConstants.MESSAGE_TYPES_IN['ImageUpdate']: self.handleImageUpdate
        }

    def run(self):
        self.logger.info('Connection accepted from {}'.format(self.address))
        try:
            while True:
                messageType = self.readInt32()
                self.messageHandlers.get(messageType, self.handleUnknownMessage)()
        except ConnectionError:
            pass
        self.sock.close()
        with self.server.lock:
            self.server.connections.remove(self)
        self.logger.info('Disconnected from {}'.format(self.address))

    def readBytes(self, count):
        data = b''
        while len(data) < count:
            newData = self.sock.recv(count-len(data))
            if not newData:
                raise ConnectionError()
            data += newData
        return data

    def readInt32(self):
        dataBytes = self.readBytes(4)
        return int.from_bytes(dataBytes, byteorder='little')

    def handleUnknownMessage(self):
        self.logger.debug('Unknown message type received from {}'.format(self.address))

    def handleServerIdRequest(self):
        self.logger.debug('ServerIdRequest received from {}'.format(self.address))
        self.sock.send(self.server.serverId)

    def handleParkingIdUpdate(self):
        self.logger.debug('ParkingIdUpdate received from {}'.format(self.address))
        parkingId = self.readInt32()
        self.parkingId = parkingId
        self.logger.debug('New ParkingId for {}: {}'.format(self.address, self.parkingId))

    def handleParkingSpotUpdate(self):
        self.logger.debug('ParkingSpotUpdate received from {}'.format(self.address))
        spotId = self.readInt32()
        state = ZyboBridgeConstants.PARKING_SPOT_STATES.get(self.readInt32(), None)
        forced = ZyboBridgeConstants.PARKING_SPOT_FORCED.get(self.readInt32(), None)
        if self.parkingId is not None:
            msg = {'type': 'ParkingSpotUpdate', 'parkingId': self.parkingId, 'spotId': spotId, 'state': state, 'forced': forced}
            self.logger.debug('Adding message from {} to queue: {}'.format(self.address, msg))
            self.server.messagesIn.put(msg)
        else:
            self.logger.debug('ParkingSpotUpdate from {} discarded, no parkingId assigned'.format(self.address))

    def handleImageUpdate(self):
        self.logger.debug('ImageUpdate received from {}'.format(self.address))
        cameraId = self.readInt32()
        imageSize = self.readInt32()
        image = self.readBytes(imageSize)
        if self.parkingId is not None:
            msg = {'type': 'ImageUpdate', 'parkingId': self.parkingId, 'cameraId': cameraId, 'image': image}
            self.logger.debug('Adding message from {} to queue'.format(self.address))
            self.server.messagesIn.put(msg)
        else:
            self.logger.debug('ImageUpdate from {} discarded, no parkingId assigned'.format(self.address))
