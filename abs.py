import time
import threading
import pyinterface

class abs_controller(object):
	buff = 0x00
	error = []
	
	position = ''
	
	
	def __init__(self, ndev=1):
		self.dio = pyinterface.create_gpg2000(ndev)
		pass
	
	def print_msg(self, msg):
		print(msg)
		return
	
	def print_error(self, msg):
		self.error.append(msg)
		self.print_msg('!!!! ERROR !!!! ' + msg)
		return
	
	def get_pos(self):
		ret = self.position = self.dio.ctrl.in_byte('FBIDIO_IN1_8')
		if ret == 0x09:
			self.position = 'IN'
		elif ret == 0x05:
			self.position = 'OUT'
		else:
			self.position = 'MOVE'
		return

	def move(self, dist):
		self.get_pos()
		if dist == 'IN':
			self.buff = 0x00
		elif dist == 'OUT':
			self.buff = 0x01
		while dist != self.position:
			self.dio.ctrl.out_byte('FBIDIO_OUT1_8', self.buff)
			self.get_pos()
		return
	
	def move_r(self):
		self.move(self, 'IN')
		return
	
	def move_sky(self):
		self.move(self, 'OUT')
		return
		
	def read_pos(self):
		return self.position
