from ArgonUtility import *


class PBOC(object):
    def __init__(self, device):
        self.device = device

    @recordmodule
    def select(self, msg=''):
        self.device.reset()

        matchdata('111', '111', 'Match Test')
        matchdata('111', '123', 'Match Test')
        matchdata('111', '111')

        self.device.sendisplay('00A4040007A0000003330101', sw=['9000'], expect_data='6F0A8408A000000333010101')
        self.device.sendisplay('00A4040007A0000003330101', sw=['6A83', '6A82'])
        self.device.sendisplay('00A4040007A0000003330101', expect_data='6F0A8408A000000333010101')
        self.device.sendisplay('00A4040007A0000003330101')
        self.device.sendisplay('00A4040007A0000003330101', 'Select Cmd')
        self.device.sendisplay('00A4040007A0000003330101', 'Select Cmd', sw=['9000', '6A82'], expect_data='6F0A8408A000000333010101')
        self.device.sendisplay('00A4040007A0000003330101', 'Select Cmd', sw=['9000', '6A82'])
        self.device.sendisplay('00A4040007A0000003330101', 'Select Cmd', expect_data='6F0A8408A000000333010102')

        matchdata('111', '123')

    @recordmodule
    def select_pass(self, msg=''):
        self.device.reset()
        self.device.sendisplay('00A4040007A0000003330101')