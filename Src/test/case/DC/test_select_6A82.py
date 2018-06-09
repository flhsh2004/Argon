from ArgonTest import *
from PBOC import *


class Select6A82(ArgonTest):
    def setUp(self):
        super().setUp()
        self.mytest = PBOC(self.device)

    def test_Select6A82_procedure(self):
        """标准测试"""
        self.begintrans('Standard Transcation')
        self.mytest.select_pass('Select Process')

    def test_Select6A82_blank_procedure(self):
        """空白测试"""
        self.begintrans('Blank Transcation')

    @skipif(True, 'I want to skip')
    def test_Select6A82_skip_procedure(self):
        """跳出测试"""
        pass
