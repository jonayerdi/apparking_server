#!/usr/bin/python

import threading

from . import ZyboBridgeConstants

class ZyboBridgeSender(threading.Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        while True:
            msg = self.server.messagesOut.get()
            if msg['type'] == 'ParkingSpotUpdate':
                with self.server.lock:
                    for conn in self.server.connections:
                        try:
                            if conn.parkingId == msg['parkingId']:
                                conn.sock.send(ZyboBridgeConstants.MESSAGE_TYPES_OUT['ParkingSpotUpdate'].to_bytes(4, byteorder='little'))
                                conn.sock.send(msg['spotId'].to_bytes(4, byteorder='little'))
                                conn.sock.send(msg['state'].to_bytes(4, byteorder='little'))
                                conn.sock.send(msg['forced'].to_bytes(4, byteorder='little'))
                        except Exception as e:
                            self.server.logger.error('Exception sending ParkingSpotUpdate: {}'.format(e))
            self.server.messagesOut.task_done()
