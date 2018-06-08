from ArgonDevice import *
from ArgonLog import *
from ctypes import *
import win32api


class USBCOMReader(ArgonDevice):
    def __init__(self):
        self.dll = ""
        self.hDev = ""
        self.ATR = ""

    @recordopen
    def openport(self, port):
        if port[0:3] == "USB":
            param1 = c_int(1)
            param2 = c_char(b"0")
            nad = c_char(0x15)
        elif port[0:3] == "COM":
            param1 = c_int(9600)
            param2 = c_char(b"E")
            nad = c_char(0x12)
        else:
            raise DeviceError('No Device ' + port)
        try:
            self.dll = windll.LoadLibrary("wdcrwv.dll")
            name = c_char_p(port.encode("utf8"))
            self.hDev = self.dll.CT_open(name, param1, param2)
            if self.hDev == -1:
                raise DeviceError('Open ' + port + 'Failed')
            else:
                self.dll.ICC_set_NAD(self.hDev,nad)
                return label_pass
        except Exception:
            raise DeviceError('Open ' + port + ' Failed')

    @recordreset
    def reset(self):
        try:
            lenresp = create_string_buffer(1)
            resp = create_string_buffer(255)
            rtn = self.dll.ICC_reset(self.hDev,lenresp, resp)
            # 返回响应码9000
            if rtn == 36864:
                self.ATR = resp.raw.hex()[0:int(lenresp.raw.hex(),16) * 2].upper()
                return self.ATR,label_pass
            else:
                raise DeviceError('Rest Device Failed')
        except Exception:
            raise DeviceError('Rest Device Failed')

    @recordapdu
    def sendisplay(self, apdudata, msg='', **kwargs):
        status = label_pass
        try:
            comm = bytes.fromhex(apdudata)
            strlen = len(comm)
            lenresp = create_string_buffer(1)
            resp = create_string_buffer(255)
            rtn = self.dll.ICC_tsi_api(self.hDev, strlen, comm, lenresp, resp)
            rtn_sw = hex(rtn)[2:].upper()
            rtn_data = resp.raw.hex()[0:int(lenresp.raw.hex(),16)*2].upper()
        except Exception:
            raise DeviceError('Send APDU Failed')
        else:
            if 'expect_data' in kwargs.keys():
                if not self.checkrespdata(rtn_data, kwargs['expect_data']):
                    status = label_fail

            if 'sw' in kwargs.keys():
                if not self.checksw(rtn_sw, kwargs['sw']):
                    status = label_fail

            return rtn_data, rtn_sw, status

    @recordclose
    def closeport(self):
        try:
            self.dll.CT_close(self.hDev)
            win32api.FreeLibrary(self.dll._handle)
            return label_pass
        except Exception:
            raise DeviceError('Close Device Failed')


if __name__ == '__main__':

    jts = USBCOMReader()
    jts.openport("USB1")
    jts.reset()
    jts.sendisplay("00A4040007A0000000041010")
    jts.sendisplay("00B2021400")
    jts.closeport()

    #resp1, rtn1, state = jts.senDisplay("00A4040007A0000000041010", "9000", "6A88",expectData="6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """
    jts.senDisplay("00A4040007A0000000041010", "9000", "6A88")

    # jts.senDisplay("00A4040007A0000000041010", "6A82")
    jts.senDisplay("00A4040007A0000000041010")

    jts.senDisplay("00A4040007A0000000041010",expectData = "6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """

    #jts.closePort()

