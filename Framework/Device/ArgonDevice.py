from ArgonLog import translog, label_error

class DeviceError(Exception):
    def __init__(self, *args):
        translog(label_error, args[0])


class DataError(Exception):
    pass


class SWError(AssertionError):
    pass


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
    def openport(self, port):
        pass

    def reset(self):
        pass

    def sendisplay(self, apdudata, msg='', **kwargs):
        pass

    def closeport(self):
        pass

    @staticmethod
    def checkrespdata(actualdata, expectdata):
        if (expectdata != '') & (expectdata != actualdata):
            return False
        else:
            return True

    @staticmethod
    def checksw(actualsw, expectsw):
        if isinstance(expectsw, list):
            for sw_param in expectsw:
                if sw_param == actualsw:
                    return True
        elif isinstance(expectsw, str):
            if expectsw == actualsw:
                return True
        else:
            raise SWError('Wrong Expect SW')
        return False

    '''
    @staticmethod
    def _showapdu(apdudata, actualdata, expectdata, actualsw, expectsw):
        expect_rtn = ""
        if len(expectsw) == 0:
            expect_rtn = "9000"
        else:
            for index in range(len(expectsw)):
                if index == 0:
                    expect_rtn = expectsw[index]
                else:
                    expect_rtn = expect_rtn + "\\" + expectsw[index]
        print("AH:" + apdudata.upper())
        if expectdata != "":
            print("ED:" + expectdata.upper())
        if actualdata != "":
            print("AD:" + actualdata.upper())
        print("ES:" + expect_rtn)
        print("AS:" + actualsw.upper())
    '''








