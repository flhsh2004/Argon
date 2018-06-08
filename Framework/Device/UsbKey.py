from ctypes import *
from ArgonDevice import *
import win32api
import os
import ctypes


class UsbKey(ArgonDevice):
    def __init__(self):
        self.dll = ""
        self.hDev = ""
        AppPosition = os.path.abspath('.')
        dllPosition = AppPosition + "//wdcrwvKey.dll"
        self.dll = ctypes.windll.LoadLibrary(dllPosition)
    def openPort(self,port):
        try:
            str = port.encode("utf8")
            name = c_char_p(str)
            self.hDev = self.dll.CT_open(name, 0, 0)
            if self.hDev == -1:
                print("KEY连接失败")
                return False
            else:
                print("KEY连接成功")
                return True
        except Exception:
            print("KEY连接失败")
            return False
    def reset(self):
        try:
            lenresp = create_string_buffer(1)
            resp = create_string_buffer(255)
            rtn = self.dll.ICC_reset(self.hDev,lenresp, resp)
            rtn = hex(rtn)[2:].upper()
            if rtn == "9000":
                len1 = int(lenresp.raw.hex(),16)
                RtnData = resp.raw.hex()[0:len1 * 2].upper()
                print("ATR:" + RtnData)
                return RtnData,True
            else:
                print("KEY复位失败")
                return False
        except Exception:
            print("KEY复位失败")
            return False

    def senDisplay(self, APDUdata, *SW,expectData = ""):
        state = True
        try:
            comm = bytes.fromhex(APDUdata)
            strlen = len(comm)
            lenresp = create_string_buffer(1)
            resp = create_string_buffer(255)
            rtn = self.dll.ICC_tsi_api(self.hDev, strlen, comm, lenresp, resp)
            rtn = hex(rtn)[2:].upper()
            len1= int(lenresp.raw.hex(),16)
            RtnData = resp.raw.hex()[0:len1*2].upper()
            WDDevice.showAPDU(APDUdata,RtnData,expectData,rtn,SW)
        except Exception:
            print("指令发送异常")
            return "", "", state
            state = False
        else:
            try:
                WDDevice.checkRespData(RtnData, expectData)
            except DataError as e:
                print(e.detail)
                # self.errorResult.append(e.detail)
                state = False
            finally:
                try:
                    WDDevice.checkSW(rtn, SW)
                except SWError as e:
                    print(e.detail)
                    # self.errorResult.append(e.detail)
                    state = False
            return RtnData, rtn, state

    def closePort(self):
        try:
            win32api.FreeLibrary(self.dll._handle)
            return True
        except Exception:
            print("KEY断开失败")
            return False

    def begintest(self):
        self.errorResult = []


if __name__ == '__main__':
    jts = UsbKey()
    jts.openPort("Flashdisk1")
    jts.reset()
    jts.senDisplay("0012000000")
    jts.senDisplay("0084000008", "9000", "6982")
    jts.senDisplay("00a40000023f00")
    jts.closePort()

    #resp1, rtn1, state = jts.senDisplay("00A4040007A0000000041010", "9000", "6A88",expectData="6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """
    jts.senDisplay("00A4040007A0000000041010", "9000", "6A88")

    # jts.senDisplay("00A4040007A0000000041010", "6A82")
    jts.senDisplay("00A4040007A0000000041010")

    jts.senDisplay("00A4040007A0000000041010",expectData = "6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """

    #jts.closePort()

