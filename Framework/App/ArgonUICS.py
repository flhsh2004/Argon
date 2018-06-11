from ArgonUtility import *

temp_tag = ['70', 'A5', 'BF0C', '61', '77', '6F']
fourlen_tag = ['5F', '9F', 'BF', 'DF']
longlen_tag = '81'


class ArgonTLVError(AssertionError):
    pass


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
        tags = self.parsetags(resp)

    # 解析TLV数据-只限tag
    def parsetags(self, data):
        temptags = []
        resp = data

        if data == '':
            raise ArgonTLVError('Void Data')

        # 找到Tag
        if resp[:2] in fourlen_tag:
            ptag = resp[:4]
            resp = resp[4:]
        else:
            ptag = resp[:2]
            resp = resp[2:]

        if resp == '':
            raise ArgonTLVError('Void Length & Value')

        # 找到Length
        if resp[:2] == longlen_tag:
            plen = resp[2:4]
            resp = resp[4:]
        else:
            plen = resp[:2]
            resp = resp[2:]

        if plen == '':
            raise ArgonTLVError('Void Length')

        # 找到Value
        pvalue = resp[:intlength(plen)]
        resp = resp[intlength(plen):]

        if intlength(plen) != len(pvalue):
            raise ArgonTLVError('Value Length Incorrect')

        # 如果是模版tag需要存储为节点
        if ptag in temp_tag:
            temptags.append({'T': ptag, 'L': plen, 'tags': []})
            # 不允许空模版出现
            if pvalue == '':
                raise ArgonTLVError('Void Template Data')
            # 其余数据需要递归
            extratags = self.parsetags(pvalue)
            for tag in extratags:
                temptags[-1]['tags'].append(tag)
        # 如果不是模版tag直接存储
        else:
            temptags.append({'T': ptag, 'L': plen, 'V': pvalue})

        # 如果还有数据进行递归
        if resp != '':
            moretags = self.parsetags(resp)
            for tag in moretags:
                temptags.append(tag)

        return temptags


if __name__ == '__main__':
    import unittest


    class TestParsetags(unittest.TestCase):
        def setUp(self):
            self.uics = ArgonUICS('Test')

        def test_correct(self):
            self.uics.parsetags('8400')
            self.uics.parsetags('8408A000000333010101')
            self.uics.parsetags('848108A000000333010101')
            self.uics.parsetags('848108A0000003330101018F0101')
            self.uics.parsetags('6F038F0101')

        def test_fail_only_value(self):
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A000000333010101')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, '6F028F01')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, '00')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, '')

        def test_fail_no_value(self):
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A003')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A0')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A03')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, '5F2')

        def test_fail_wrong_length(self):
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A009000333010101')
            self.assertRaises(ArgonTLVError, self.uics.parsetags, '9F7D010102')

        def test_fail_temp_no_value(self):
            self.assertRaises(ArgonTLVError, self.uics.parsetags, 'A500')

    unittest.main(verbosity=2)
