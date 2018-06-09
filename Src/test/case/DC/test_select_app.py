from ArgonTest import *
from PBOC import *


class TestSelectApp(ArgonTest):
    def setUp(self):
        super().setUp()
        self.mytest = PBOC(self.device)

    def test_standard_procedure(self):
        """标准测试"""
        self.begintrans('Standard Transcation')
        self.mytest.select('Select Process')

    def test_standard_skip_procedure(self):
        """跳出测试"""
        self.skipTest('Skip Test')

    def test_standard_blank_procedure(self):
        """空白测试"""
        self.begintrans('Blank Transcation')

    # @skipif(True, 'skipIf')
    def test_standard_fail(self):
        """失败测试"""
        # raise AssertionError('')
        raise ArgonLogError('Error')
        self.mytest.select('Select Process')
