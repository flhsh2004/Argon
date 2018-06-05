from APDU import *


class PBOC(object):
    def __init__(self, device):
        self.device = device

    @recordmodule
    def select(self, msg=''):
        self.device.reset()

        matchdata('111', '111', 'Match Test')
        matchdata('111', '123', 'Match Test')
        matchdata('111', '111')

        self.device.senDisplay('00A4040008A000000333010101', SW=['9000'], expectData='6F0A8408A000000333010101')
        self.device.senDisplay('00A4040008A000000333010101', SW=['6A83', '6A82'])
        self.device.senDisplay('00A4040008A000000333010101', expectData='6F0A8408A000000333010101')
        self.device.senDisplay('00A4040008A000000333010101')
        self.device.senDisplay('00A4040008A000000333010101', 'Select Cmd')
        self.device.senDisplay('00A4040008A000000333010101', 'Select Cmd', SW=['9000', '6A82'], expectData='6F0A8408A000000333010101')
        self.device.senDisplay('00A4040008A000000333010101', 'Select Cmd', SW=['9000', '6A82'])
        self.device.senDisplay('00A4040008A000000333010101', 'Select Cmd', expectData='6F0A8408A000000333010102')

        matchdata('111', '123')