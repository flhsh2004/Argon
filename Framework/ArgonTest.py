import unittest
import functools

from MyDevice import *
from ArgonLog import *


class ArgonTest(unittest.TestCase):
    def setUp(self):
        initlog(self._testMethodName)
        translog('Info', 'Establish Context')

        try:
            workdir = os.getcwd()
            workdir = workdir[:workdir.find(logdir)]

            stream = open(workdir + 'Config\\device.yml', 'r')
            data = yaml.load(stream)
            stream.close()

            self.device = mydevice(data[0]['type'])
            self.device.openport(data[0]['port'])
        except Exception:
            savecaselog()
            raise


    def tearDown(self):
        if not self._outcome.errors[-1][1] is None:
            err = self._outcome.errors[-1][1][1]
            if isinstance(err, self.failureException):
                err_type = label_fail
            else:
                err_type = label_error

            if len(err.args) == 0:
                err_msg = 'Unnamed ' + err_type
            elif err.args[0] == '':
                err_msg = 'Unnamed ' + err_type
            else:
                err_msg = err.args[0]

            try:
                log_all.append({'level': level_trans,
                                'status': err_type,
                                'msg': err_msg,
                                'module': []})
            except Exception:
                raise ArgonLogError('No Log Root')

        translog('Info', 'Release Context')
        try:
            self.device.closeport()
        except Exception:
            savecaselog()
            raise
        else:
            if not getcasepass():
                self.fail('Case [' + self._testMethodName + '] Failed. Please Check Case Log!')
        finally:
            savecaselog()

    @staticmethod
    def begintrans(msg):
        translog(label_info, msg)

    @staticmethod
    def beginmodule(msg):
        modulelog(msg)

    def skipTest(self, reason):
        raise ArgonSkipTest(reason)

    def fail(self, msg=None):
        if (msg is None) | (msg == ''):
            msg = 'Unnamed Failure'
        translog(label_fail, msg)
        super().fail(msg)

    @staticmethod
    def info(msg):
        matchlog(label_info, msg)

    @staticmethod
    def warning(msg):
        matchlog(label_warning, msg)


class ArgonSkipTest(unittest.SkipTest):
    """日志保存处理类"""
    def __init__(self, *args):
        translog(label_skip, args[0])


def _id(obj):
    return obj


def skip(reason):
    """
    Unconditionally skip a test.
    """
    def decorator(test_item):
        if not isinstance(test_item, type):
            @functools.wraps(test_item)
            def skip_wrapper():
                raise ArgonSkipTest(reason)
            test_item = skip_wrapper

        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason

        initlog(test_item.__name__)
        translog(label_skip, reason)
        savecaselog()

        return test_item
    return decorator


def skipif(condition, reason):
    """
    Skip a test if the condition is true.
    """
    if condition:
        return skip(reason)
    return _id


def skipunless(condition, reason):
    """
    Skip a test unless the condition is true.
    """
    if not condition:
        return skip(reason)
    return _id
