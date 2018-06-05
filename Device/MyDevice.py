from PCSCReader import *
from USBCOMReader import *


def MyDevice(name):
    if name == "USB" or name == "COM":
        device = USBCOMReader()
        return device
    elif name == "PCSC":
        device = PCSCReader()
        return device
    else:
        pass


if __name__ == '__main__':
    jts = MyDevice('USB')
    jts.openPort("USB1")
    jts.reset()
    resp = jts.senDisplay("00A4040007A0000000041010", "9000", "6A82", "6A83")
    jts.closePort()
