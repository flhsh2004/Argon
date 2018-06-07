from ctypes import *
from ArgonDevice import *
import win32api


class USBCOMReader(ArgonDevice):
    def __init__(self):
        self.dll = ""
        self.hDev = ""

    def openPort(self, port):
        if port[0:3] == "USB":
            param1 = c_int(1)
            param2 = c_char(b"0")
            nad = c_char(0x15)
        elif port[0:3] == "COM":
            param1 = c_int(9600)
            param2 = c_char(b"E")
            nad = c_char(0x12)
        else:
            print("读卡器不支持")
            return False
        try:
            self.dll = windll.LoadLibrary("wdcrwv.dll")
            str = port.encode("utf8")
            name = c_char_p(str)
            self.hDev = self.dll.CT_open(name, param1, param2)
            if self.hDev == -1:
                print("读卡器连接失败")
                return False
            else:
                print("读卡器连接成功")
                self.dll.ICC_set_NAD(self.hDev,nad)
                return True
        except Exception:
            print("读卡器连接失败")
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
                print("复位失败")
                return "",False
        except Exception:
            print("复位失败")
            return "",False

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
            ArgonDevice.showAPDU(APDUdata,RtnData,expectData,rtn,SW)
        except Exception:
            print("指令发送异常")
            state = False
            return "", "", state
        else:
            try:
                ArgonDevice.checkRespData(RtnData, expectData)
            except DataError as e:
                print(e.detail)
                # self.errorResult.append(e.detail)
                state = False
            finally:
                try:
                    ArgonDevice.checkSW(rtn, SW)
                except SWError as e:
                    print(e.detail)
                    # self.errorResult.append(e.detail)
                    state = False
            return RtnData, rtn, state

    def closePort(self):
        try:
            self.dll.CT_close(self.hDev)
            win32api.FreeLibrary(self.dll._handle)
            return True
        except Exception:
            print("读卡器断开失败")
            return False


if __name__ == '__main__':

    #for num in range(0,1):
    jts = USBCOMReader()
    jts.openPort("USB1")
    jts.reset()
    jts.senDisplay("00A4040007A0000000041010")
    jts.senDisplay("00B2021400")
    jts.closePort()

    #resp1, rtn1, state = jts.senDisplay("00A4040007A0000000041010", "9000", "6A88",expectData="6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """
    jts.senDisplay("00A4040007A0000000041010", "9000", "6A88")

    # jts.senDisplay("00A4040007A0000000041010", "6A82")
    jts.senDisplay("00A4040007A0000000041010")

    jts.senDisplay("00A4040007A0000000041010",expectData = "6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """

    #jts.closePort()

