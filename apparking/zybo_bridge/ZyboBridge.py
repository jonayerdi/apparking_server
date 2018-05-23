#!/usr/bin/python

import threading
import socket
import queue
import logging

from .ZyboBridgeConnection  import ZyboBridgeConnection
from .ZyboBridgeSender  import ZyboBridgeSender

class ZyboBridge(threading.Thread):
	def __init__(self, serverId=b'\x00000000', ip='127.0.0.1', port=6969, logger=logging.getLogger()):
		super().__init__()
		self.logger = logger
		self.serverId = serverId
		self.ip = ip
		self.port = port
		self.sock = None
		self.sender = None
		self.connections = []
		self.lock = threading.Lock()
		self.messagesIn = queue.Queue(maxsize=64)
		self.messagesOut = queue.Queue(maxsize=64)

	def run(self):
		# Setup server socket
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((self.ip, self.port))
			self.sock.listen()
		except Exception as e:
			self.logger.error('Exception binding socket: {}'.format(e))
			return
		# Init messages sender
		self.sender = ZyboBridgeSender(self)
		self.sender.start()
		# Accept connections
		self.logger.info('Accepting connections to {}:{}'.format(self.ip, self.port))
		try:
			while True:
				conn, addr = self.sock.accept()
				connection = ZyboBridgeConnection(self, conn, addr)
				with self.lock:
					self.connections.append(connection)
				connection.start()
		except Exception as e:
			self.logger.error('Exception accepting connections: {}'.format(e))
		finally:
			self.sock.close()

if __name__ == "__main__":
	log = logging.getLogger('ZyboBridge')
	log.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(name)s(%(levelname)s): %(message)s')
	ch.setFormatter(formatter)
	log.addHandler(ch)
	zyboBridge = ZyboBridge(serverId=b'\x00000000', ip='127.0.0.1', port=6969, logger=log)
	zyboBridge.start()
	while True:
		print(zyboBridge.messagesIn.get())
		zyboBridge.messagesIn.task_done()
		msg = {'type': 'ParkingSpotUpdate', 'parkingId': 0, 'spotId': 12, 'state': 2, 'forced': 0}
		zyboBridge.messagesOut.put(msg)
