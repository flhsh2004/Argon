from ArgonTest import *
from PBOC import *


class Select6A82(ArgonTest):
    def setUp(self):
        super().setUp()
        self.mytest = PBOC(self.device)

    def test_Select_61xx(self):
        """标准测试"""
        self.begintrans('Standard Transcation')
        self.mytest.select_test_61xx('Select Process')

