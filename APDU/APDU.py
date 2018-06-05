from ArgonLog import *


@recordmatch
def matchdata(Data, expectData, msg=''):
    if Data != expectData:
        status = 'Fail'
    else:
        status = 'Pass'
    return status


class PCSCReader(object):
    def __init__(self):
        pass

    @recordopen
    def openPort(self, port):
        return 'Pass'

    @recordclose
    def closePort(self):
        return 'Pass'

    @recordreset
    def reset(self):
        return '3B1096', 'Pass'

    @recordapdu
    def senDisplay(self, APDUdata, msg='', **kwargs):
        status = 'Pass'

        RtnData = '6F0A8408A000000333010101'
        rtn = '9000'

        if 'expectData' in kwargs.keys():
            if (kwargs['expectData'] != '') & (RtnData != kwargs['expectData']):
                status = 'Fail'

        def checksw(prtn, pSW):
            if isinstance(pSW, list):
                for sw_param in pSW:
                    if sw_param == prtn:
                        return True
            elif isinstance(pSW, str):
                if pSW == prtn:
                    return True
            else:
                raise ArgonLogError('Wrong SW Type')
            return False

        if 'SW' in kwargs.keys():
            if not checksw(rtn, kwargs['SW']):
                status = 'Fail'

        return RtnData, rtn, status


if __name__ == '__main__':
    initlog('APDU')

    reader = PCSCReader()

    translog('Transcation First')
    modulelog('Select Application')

    reader.openPort('USB', 'Open Port')
    reader.reset('Reset')
    reader.senDisplay('00A4040008A000000333010101', ['9000', '6A82'], '6F0A8408A000000333010101', 'Select Cmd')
    reader.senDisplay('00A4040008A000000333010101', '9000', '6F0A8408A000000333010101', 'Select Cmd')

    reader.closePort('Close Port')

    translog('Transcation First')
    modulelog('Select Application')

    reader.openPort('USB', 'Open Port')
    reader.reset('Reset')
    reader.senDisplay('00A4040008A000000333010101', ['9000', '6A82'], '', 'Select Cmd')
    reader.senDisplay('00A4040008A000000333010101', '9000', '6F0A8408A000000333010101', 'Select Cmd')

    reader.closePort('Close Port')

    savecaselog()
