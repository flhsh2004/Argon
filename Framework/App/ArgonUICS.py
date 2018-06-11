from ArgonUtility import *

temp_tag = ['70', 'A5', 'BF0C', '61', '77', '6F']
fourlen_tag = ['5F', '9F', 'BF', 'DF']
longlen_tag = '81'


class ArgonUICS(object):
    def __init__(self, device):
        self.device = device

    @recordmodule
    def select(self, msg=''):
        self.device.reset()
        self.select_cmd('A000000333010101')

    def select_cmd(self, data):
        apdu = '00A40400' + addlength(data)
        resp, sw = self.device.sendisplay(apdu, 'Select Cmd')
        self.parsetags(resp)

    @staticmethod
    def parsetags(data):
        tags = []
        temptags = tags
        resp = data

        while resp != '':
            # 找到Tag
            if resp[:2] in fourlen_tag:
                ptag = resp[:4]
                resp = resp[4:]
            else:
                ptag = resp[:2]
                resp = resp[2:]

            # 找到Length
            if resp[:2] == longlen_tag:
                plen = resp[2:4]
                resp = resp[4:]
            else:
                plen = resp[:2]
                resp = resp[2:]

            # 找到Value
            pvalue = resp[:intlength(plen)]
            resp = resp[intlength(plen):]

            # 如果是模版tag需要存储为节点
            if ptag in temp_tag:
                temptags.append({'T': ptag, 'L': plen, 'tags': []})
                resp = pvalue
                temptags = temptags[-1]['tags']
            else:
                temptags.append({'T': ptag, 'L': plen, 'V': pvalue})

        return tags


if __name__ == '__main__':
    import unittest


    class TestParsetags(unittest.TestCase):
        def setUp(self):
            self.uics = ArgonUICS('Test')

        def test_correct(self):
            self.uics.parsetags('8408A000000333010101')

        def test_fail_only_value(self):
            self.uics.parsetags('A000000333010101')

    unittest.main()
