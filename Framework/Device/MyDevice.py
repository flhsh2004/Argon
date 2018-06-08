from PCSCReader import *
from USBCOMReader import *
from UsbKey import *
from UsbKeysoket import *


def mydevice(name):
    if name == "USB" or name == "COM":
        device = USBCOMReader()
        return device
    elif name == "PCSC":
        device = PCSCReader()
        return device
    elif name == 'soket':
        device = UsbKeysoket()
        return device
    elif name == 'CCID' or name == 'Flashdisk':
        device = UsbKey()
        return device
    else:
        pass
