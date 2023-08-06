"""."""
from time import time
from pyzabbix import ZabbixMetric, ZabbixSender


class ZabbixLogger():

    def __init__(self, idx, address, port=None, use_config=None):
        if port:
            self._sender = ZabbixSender(address, port, use_config=use_config)
        else:
            self._sender = ZabbixSender(address, use_config=use_config)
        self._idx = idx

    def push(self, key, value, timestamp=None):
        if not isinstance(timestamp, (float, int)):
            timestamp = None
        packet = [
            ZabbixMetric(self._idx, key, value, timestamp)
        ]
        self._sender.send(packet)
