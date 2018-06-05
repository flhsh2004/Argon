class DataError(AssertionError):
    def __init__(self,actualData,expectData):
        self.ID = "DataError"
        self.detail = "响应数据错误，期望返回"+ expectData + "，实际返回" + actualData


class SWError(AssertionError):
    def __init__(self, actualSW,expectSW):
        self.ID = "SWError"
        self.detail = "响应码错误，期望返回"+ expectSW + "，实际返回" + actualSW


class ResultError(Exception):
    def __init__(self, Error):
        SWdict = {
            "6A82":"文件\应用选择失败",
            "6A84": "空间不足",
            "6988": "MAC错误",
            "6A88": "不存在",
            "ADERROR":"响应数据错误",
            "SHOWERROR":"数据检查错误"
        }
        self.describe = SWdict.get(Error)


class ArgonDevice(object):
    def openPort(self,port):
        pass

    def reset(self):
        pass

    def senDisplay(self,APDUdata, *SW, expectData = ""):
        pass

    def closePort(self):
        pass

    @staticmethod
    def checkRespData(actualData,expectData):
        if expectData != "":
            if actualData != expectData:
                raise DataError(actualData,expectData)

    @staticmethod
    def checkSW(actualSW,expectSW):
        SWTag = False
        if len(expectSW) == 0:
            expectRtn = "9000"
            if actualSW == "9000":
                SWTag = True
        else:
            for index in range(len(expectSW)):
                if index == 0:
                    expectRtn = expectSW[index]
                else:
                    expectRtn = expectRtn + "\\" + expectSW[index]
                if actualSW == expectSW[index]:
                    SWTag = True
        if SWTag == False:
            raise SWError(actualSW, expectRtn)

    @staticmethod
    def showAPDU(APDUdata,actualData,expectData,actualSW,expectSW):
        expectRtn = ""
        if len(expectSW) == 0:
            expectRtn = "9000"
        else:
            for index in range(len(expectSW)):
                if index == 0:
                    expectRtn = expectSW[index]
                else:
                    expectRtn = expectRtn + "\\" + expectSW[index]
        print("AH:"+APDUdata.upper())
        if expectData != "":
            print("ED:" + expectData.upper())
        if actualData != "":
            print("AD:" + actualData.upper())
        print("ES:"+ expectRtn)
        print("AS:"+actualSW.upper())









