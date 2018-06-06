from ArgonDivice import *
from ArgonLog import *
from smartcard.scard import *
from smartcard.System import readers
from smartcard.util import toHexString, toBytes, PACK


class PCSCReader(ArgonDevice):
    def __init__(self):
        self.connection = ''
        self.ATR = ''

    @recordopen
    def openport(self, port):
        for reader in readers():
            if reader.name == port:
                try:
                    self.connection = reader.createConnection()
                    self.connection.connect()
                    self.ATR = toHexString(self.connection.getATR(), PACK)
                    return label_pass
                except Exception:
                    raise DeviceError('Open ' + port + 'Failed')
        raise DeviceError('No Device ' + port)

    @recordreset
    def reset(self):
        try:
            SCardReconnect(self.connection.component.hcard, SCARD_SHARE_EXCLUSIVE,
                           SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1, SCARD_RESET_CARD)

            # TODO 需要删除print
            # print("ATR:" + self.ATR)

            return self.ATR, label_pass
        except Exception:
            raise DeviceError('Rest Device Failed')

    @recordapdu
    def sendisplay(self, apdudata, msg='', **kwargs):
        # 发送指令处理状态
        status = label_pass
        try:
            response, sw1, sw2 = self.connection.transmit(toBytes(apdudata))
            rtn_data = toHexString(response, PACK)
            rtn_sw = toHexString([sw1, sw2], PACK)

            # TODO 需要删除该语句
            # self._showapdu(apdudata, rtn_data, kwargs['expectData'], rtn_sw, kwargs['SW'])

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
            self.connection.disconnect()
            return label_pass
        except Exception:
            raise DeviceError('Close Device Failed')


if __name__ == '__main__':
    jts = PCSCReader()
    jts.openport("Identiv uTrust 4700 F CL Reader 1")
    jts.reset()
    jts.sendisplay("00A4040007A0000003330101", 'Test', SW='9000', expectData='0000')
    jts.closeport()

