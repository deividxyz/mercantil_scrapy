import logging
import sys
import socket
import time
import requests
import stem
import stem.control

# Tor settings
TOR_ADDRESS = "127.0.0.1"
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = "my password"

# Privoxy settings
PRIVOXY_ADDRESS = "127.0.0.1" 	# This assumes this code is running in a Docker-Compose service linked to the "privoxy" service
PRIVOXY_PORT = 8118 			# This is determined by the "listen-address" in Privoxy's "config" file
HTTP_PROXY = 'http://{address}:{port}'.format(address=PRIVOXY_ADDRESS, port=PRIVOXY_PORT)

logger = logging.getLogger(__name__)


class TorController(object):
	def __init__(self):
		self.controller = stem.control.Controller.from_port(address=TOR_ADDRESS, port=TOR_CONTROL_PORT)
		self.controller.authenticate(password=TOR_PASSWORD)
		self.session = requests.Session()
		self.session.proxies = {'http': HTTP_PROXY}

	def request_ip_change(self):
		self.controller.signal(stem.Signal.NEWNYM)

	def get_ip(self):
		'''Check what the current IP address is (as seen by IPEcho).'''
		return self.session.get('http://icanhazip.com/').text

	def change_ip(self):
		'''Signal a change of IP address and wait for confirmation from IPEcho.net'''
		current_ip = self.get_ip()
		logger.debug("Initializing change of identity from the current IP address, {current_ip}".format(current_ip=current_ip))
		self.request_ip_change()
		while True:
			new_ip = self.get_ip()
			if new_ip == current_ip:
				logger.debug("The IP address is still the same. Waiting for 5 seconds before checking again...")
				time.sleep(5)
			else:
				break
		logger.debug("The IP address has been changed from {old_ip} to {new_ip}".format(old_ip=current_ip, new_ip=new_ip))
		return new_ip

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.controller.close()


def change_identity():
    with TorController() as tor_controller:
        tor_controller.change_ip()
