from ArgonTest import *
from ArgonUICS import *


class SelectStandard(ArgonTest):
    def setUp(self):
        super().setUp()
        self.mytest = ArgonUICS(self.device)

    def test_standard_procedure(self):
        """标准测试"""
        self.begintrans('Standard Transcation')
        self.mytest.select('Select Cmd')
