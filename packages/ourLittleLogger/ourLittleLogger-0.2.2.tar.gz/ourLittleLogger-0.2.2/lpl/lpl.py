"""Logger for connectome python projects."""
import logging
from .zabbix_logger import ZabbixLogger

def getLogger(idx='connectome_module', level=logging.DEBUG):
    """Get logger with specified logger name."""
    fmt = '%(asctime)s.%(msecs)03d | %(name)s | [%(levelname)s]: %(message)s'
    datefmt = '%d-%m-%Y %H:%M:%S'
    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)
    logger = logging.getLogger(idx)
    return logger

def getZabbixLogger(idx, address):
    """Get zabbix logger with specified logger name and address."""
    return ZabbixLogger(idx, address)
