import requests

from stem import Signal
from stem.control import Controller

chequeo = requests.get('https://icanhazip.com/', proxies={'https': '127.0.0.1:8118'})

ip_vieja = chequeo.text.strip()
print('ip vieja: ' + ip_vieja)
with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='my password')
        controller.signal(Signal.NEWNYM)

chequeo = requests.get('https://icanhazip.com/', proxies={'https': '127.0.0.1:8118'})
ip_nueva = chequeo.text.strip()
print('ip nueva: ' + ip_nueva)
