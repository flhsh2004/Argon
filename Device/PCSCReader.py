from ArgonDivice import *
from smartcard.scard import *
from smartcard.System import readers
from smartcard.util import toHexString, toBytes


class PCSCReader(ArgonDevice):
    def __init__(self):
        self.connection = ""
        # self.result = True

    def openPort(self,port):
        creaders = readers()
        for index in range(len(creaders)):
            if creaders[index].name == port:
                try:
                    self.connection = creaders[index].createConnection()
                    self.connection.connect()
                    print("PCSC读卡器连接成功")
                    return True
                except Exception:
                    print("PCSC读卡器连接失败")
                    return False
        print("PCSC读卡器连接失败")
        return False


    def reset(self):
        try:
            SCardReconnect(self.connection.component.hcard, SCARD_SHARE_SHARED, SCARD_PROTOCOL_RAW, SCARD_RESET_CARD)
            self.connection.connect()
            Response = self.connection.getATR()
            RtnData = toHexString(Response)
            RtnData = RtnData.replace(" ", "")
            print("ATR:" + RtnData)
            return RtnData,True
        except Exception:
            print("复位失败")
            return "",False

    def senDisplay(self,APDUdata, *SW,expectData = ""):
        state = True
        try:
            apdu = toBytes(APDUdata)
            Response, sw1, sw2 = self.connection.transmit(apdu)
            rtn = toHexString([sw1, sw2],1)
            RtnData = toHexString(Response,1)
            self.showAPDU(APDUdata, RtnData, expectData, rtn, SW)

        except Exception:
            print("指令发送异常")
            state = False
            return "", "", state

        else:
            try:
                self.checkRespData(RtnData, expectData)
            except DataError as e:
                print(e.detail)
                #self.errorResult.append(e.detail)
                state = False
            finally:
                try:
                    self.checkSW(rtn, SW)
                except SWError as e:
                    print(e.detail)
                    #self.errorResult.append(e.detail)
                    state = False
            return RtnData,rtn,state

    def closePort(self):
        try:
            self.connection.disconnect()
            return True
        except Exception:
            print("PCSC读卡器断开失败")
            return False


if __name__ == '__main__':
    jts = PCSCReader()
    jts.openPort("Identiv uTrust 4700 F CL Reader 0")
    jts.reset()

    """
    resp1, rtn1 = jts.senDisplay("00A4040007A0000000041010", "9000", "6A88",expectData="6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")

    jts.senDisplay("00A4040007A0000000041010", "9000", "6A88")

    # jts.senDisplay("00A4040007A0000000041010", "6A82")
    jts.senDisplay("00A4040007A0000000041010")

    data,rtn = jts.senDisplay("00A4040007A0000000041010",expectData = "6F3D8407A0000000041010A532500A4D6173746572636172648701019F1101019F120A4D617374657263617264BF0C0F9F4D020B0A9F6E0701560000303000")
    """
    jts.senDisplay("00A4040007A0000000041010", "6A89", expectData="6988")
    jts.closePort()

