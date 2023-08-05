import logging as log
import os
import serial
import socket
from time import sleep
from subprocess import check_output
from threading import Thread
from tornado.ioloop import IOLoop as IO

from wspr.upgrade import software_upgrade, firmware_upgrade
from wspr.wire_format import for_wire, from_wire
if os.environ.get('WSPR_EMULATOR'):
	from wspr.emulator import Serial, GPIO
else:
	from serial import Serial
	import RPi.GPIO as GPIO

class Monitor:
	def __init__(self, router):
		self.router = router

		log.debug('connecting to serial port...')
		self.serial = Serial(
			port='/dev/ttyAMA0',
			baudrate=115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		log.debug('connected')

		self.handlers = {
			'H': self.handle_hostname,
			'I': self.handle_ip,
			'C': self.handle_callsign,
			'G': self.handle_gps,
			'L': self.handle_locator,
			'P': self.handle_power,
			'B': self.handle_bandhop,
			'D': self.handle_tx_disable,
			'X': self.handle_tx_percentage,
			'V': self.handle_version,
			'S': self.handle_status,
			'T': self.handle_timestamp,
			'U': self.handle_software_upgrade,
			'F': self.handle_firmware_upgrade,
			'A': self.handle_heartbeat
		}

		self.startup_messages = [
			('C', ''),
			('G', ''),
			('L', ''),
			('P', ''),
			('B', ''),
			('D', ''),
			('X', ''),
			('V', ''),
			('S', ''),
			('T', '')
		]

		self.state_commands = {
			'callsign': 'C',
			'locator': 'L',
			'power': 'P',
			'tx_percentage': 'X',
			'tx_disable': 'D',
			'bandhop': 'B'
		}

		self.heartbeat_high = False
		self.heartbeat_port = 5
		self.reset_port = 17
		self.program_port = 27

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.heartbeat_port, GPIO.OUT)
		GPIO.setup(self.reset_port, GPIO.OUT)
		GPIO.setup(self.program_port, GPIO.OUT)

		# populate hostname and IP for the frontend
		self.handle_hostname(None)
		self.handle_ip(None)

	def handle_hostname(self, data):
		log.debug('retrieving hostname...')
		hostname = socket.gethostname()
		log.debug('hostname was %s', hostname)
		self.router.set_from_hardware('hostname', hostname)
		return ('H', hostname)

	def handle_ip(self, data):
		log.debug('retrieving IP...')
		ip = check_output(['hostname' , '-I'])\
			.decode('ascii')\
			.strip()\
			.split(' ')[0]
		log.debug('IP was %s', ip)
		self.router.set_from_hardware('ip', ip)
		return ('I', ip)

	def handle_callsign(self, data):
		self.router.set_from_hardware('callsign', data)

	def handle_gps(self, data):
		self.router.set_from_hardware('gps', data)

	def handle_locator(self, data):
		self.router.set_from_hardware('locator', data)

	def handle_power(self, data):
		self.router.set_from_hardware('power', int(data))

	def handle_bandhop(self, data):
		self.router.set_from_hardware('bandhop', data.split(','))

	def handle_tx_disable(self, data):
		self.router.set_from_hardware('tx_disable', data.split(','))

	def handle_tx_percentage(self, data):
		self.router.set_from_hardware('tx_percentage', int(data))

	def handle_version(self, data):
		self.router.set_from_hardware('version', data)

	def handle_status(self, data):
		self.router.set_from_hardware('status', data)

	def handle_timestamp(self, data):
		log.debug('setting the system time to %s...', data)
		check_output(['date', '-d', data])
		log.debug('time set')

	def upgrade_log(self, message):
		log.debug(message)
		self.router.upgrade_log(message)

	def restart(self):
		log.debug("cleaning up...")
		self.cleanup()
		log.debug("running exec()...")
		os.execlp("wspr-server", "wspr-server")
		# process replaced, job done
		
	def handle_software_upgrade(self, data):
		log.info("software upgrade start...")
		self.upgrade_log("upgrading software...")
		self.reset(True)
		if software_upgrade(self.upgrade_log):
			log.info("...software upgrade complete")
			self.upgrade_log("upgrade complete - restarting...")
			self.router.upgrade_success()
			self.reset(False)
			self.restart()
		else:
			log.info("...software upgrade failed")
			self.upgrade_log("upgrade failed :-(")

	def handle_firmware_upgrade(self, data):
		log.info("firmware upgrade start...")
		self.upgrade_log("upgrading firmware...")

		# hardware program invocation
		def program_mode():
			self.upgrade_log("putting PIC into program mode...")
			self.program(True)
			self.reset(True)
			self.reset(False)
			self.program(False)
			self.upgrade_log("...PIC in program mode")

		if firmware_upgrade(self.upgrade_log, program_mode):
			log.info("...firmware upgrade complete")
			self.upgrade_log("upgrade complete - restarting...")
			self.router.upgrade_success()
			self.restart()
		else:
			log.info("...firmware upgrade failed")
			self.upgrade_log("upgrade failed :-(")

	def handle_heartbeat(self, data):
		self.router.heartbeat()
		
	def send_data(self, command, rest):
		formatted = for_wire(command, rest)
		self.serial.write(formatted)
		log.debug('command sent: %s%s', command, rest)

	def route_command(self, data):
		command, rest = from_wire(data)
		log.debug('command received: %s%s', command, rest)

		handler = None
		try:
			handler = self.handlers[command]
		except KeyError:
			log.warning('no handler for %s', command)
			return

		returned = handler(rest)
		if returned is not None:
			self.send_data(*returned)
		
	def manage_serial(self):
		log.debug('sending startup messages...')
		for message in self.startup_messages:
			self.send_data(*message)
		log.debug('startup messages sent')

		log.debug('starting message receive loop...')
		while True:
			data = self.serial.readline()
			IO.current().add_callback(self.route_command, data)

	def go(self):
		self.heartbeat()
		Thread(target=self.manage_serial, daemon=True).start()

	def on_state_change(self, key, value):
		if key in {'bandhop', 'tx_disable'}:
			value = ','.join(value)
		self.send_data(self.state_commands[key], value)

	def software_upgrade(self):
		self.send_data('U', '')

	def firmware_upgrade(self):
		self.send_data('F', '')

	def heartbeat(self):
		self.heartbeat_high = not self.heartbeat_high
		GPIO.output(
			self.heartbeat_port,
			GPIO.HIGH if self.heartbeat_high else GPIO.LOW
		)

	def reset(self, high):
		log.debug("setting reset pin = %d", high)
		GPIO.output(
			self.reset_port,
			GPIO.HIGH if high else GPIO.LOW
		)
		sleep(0.1)

	def program(self, high):
		if not high:
			sleep(0.1)
		log.debug("setting program pin = %d", high)
		GPIO.output(
			self.program_port,
			GPIO.HIGH if high else GPIO.LOW
		)
		sleep(0.1)

	def cleanup(self):
		GPIO.cleanup()
