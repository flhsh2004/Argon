from PCSCReader import *
from USBCOMReader import *


def mydevice(name):
    if name == "USB" or name == "COM":
        device = USBCOMReader()
        return device
    elif name == "PCSC":
        device = PCSCReader()
        return device
    else:
        pass
