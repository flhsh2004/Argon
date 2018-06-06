from ArgonTest import *
from PBOC import *


class SubTest(ArgonTest):
    def setUp(self):
        super().setUp()
        self.mytest = PBOC(self.device)

    def test_standard_procedure(self):
        self.begintrans('Standard Transcation')
        self.mytest.select('Select Process')

    def test_skip_procedure(self):
        self.skipTest('Skip Test')

    def test_standard_blank(self):
        self.begintrans('Blank Transcation')

    # @skipif(True, 'skipIf')
    def test_standard_fail(self):
        # raise AssertionError('')
        raise ArgonLogError('Error')
        self.mytest.select('Select Process')
