import yaml
import os

# 存储单个脚本的日志内容
log_all = []
# 存储单个脚本的状态
casepass = True
# 单个脚本名称
casename = ''
# 日志存放位置
logdir = 'Test\\Case'
# 项目位置
projectdir = ''

# 存储各个节点状态
label_pass = 'Pass'
label_fail = 'Fail'
label_warning = 'Warning'
label_error = 'Error'
label_info = 'Info'
label_skip = 'Skip'

# 存储各个节点的存储等级
level_trans = '1'
level_module = '2'
level_match = '3'


def initlog(name):
    """初始化log存储名"""
    global casename
    global casepass
    global projectdir

    casepass = True
    casename = name
    log_all.clear()

    ipath = os.getcwd().find(logdir)
    if ipath > 0:
        projectdir = os.getcwd()[:ipath]
    else:
        projectdir = os.path.abspath('..') + '\\'

    return projectdir


def getcasepass():
    return casepass


def savecaselog():
    """保存log并清空临时变量"""
    global casename
    global casepass
    global projectdir
    try:
        stream = open(projectdir + 'Log\\' + casename + '.yml', 'w')
        yaml.dump(log_all, stream)
        stream.close()
    except Exception:
        raise Exception('Log Save Error')
    finally:
        log_all.clear()
        casename = ''
        casepass = True
        projectdir = ''


def translog(status, msg=''):
    """交易日志"""
    try:
        log_all.append({'level': level_trans,
                        'status': status,
                        'msg': msg,
                        'module': []})
    except Exception:
        raise ArgonLogError('No Log Root')


class ArgonLogError(Exception):
    """日志保存处理类"""
    pass


def modulelog(msg=''):
    """模块日志"""
    try:
        log_trans = log_all[-1]
    except Exception:
        raise ArgonLogError('No Trans Node')

    log_trans['module'].append({'level': level_module,
                                'status': label_info,
                                'msg': msg,
                                'list': []})

    if log_trans['status'] == label_info:
        log_trans['status'] = label_pass


def matchlog(status, msg='match string', *args):
    """指令/比较日志"""

    # 判断是否含有Trans节点
    try:
        log_trans = log_all[-1]
    except Exception:
        raise ArgonLogError('No Trans Node')

    # 判断是否含有Module节点
    try:
        log_module = log_trans['module'][-1]
    except Exception:
        raise ArgonLogError('No Module Node')

    # 判断为Error状态则抛出异常
    if status == label_error:
        raise ArgonLogError(msg)
    elif status == label_fail:
        global casepass
        casepass = False

    # 有子节点则修改默认Info状态
    if log_module['status'] == label_info:
        log_module['status'] = label_pass

    # 子节点有Fail状态则置父节点状态
    if status == label_fail:
        log_trans['status'] = label_fail
        log_module['status'] = label_fail

    # 写入Log
    try:
        # 比较节点
        if len(args) == 2:
            log_module['list'].append({'level': level_match,
                                       'status': status,
                                       'msg': msg,
                                       'a-value': args[0],
                                       'r-value': args[1]})
        # APDU节点
        elif len(args) == 5:
            log_module['list'].append({'level': level_match,
                                       'status': status,
                                       'msg': msg,
                                       'send': args[0],
                                       'a-recv': args[1],
                                       'r-recv': args[2],
                                       'a-SW': args[3],
                                       'r-SW': args[4]})
        # 一般状态节点
        elif len(args) == 0:
            log_module['list'].append({'level': level_match,
                                       'status': status,
                                       'msg': msg})
        else:
            raise TypeError

    except TypeError:
        log_module['list'].append({'level': level_match,
                                   'status': label_warning,
                                   'msg': 'Param Illegal'})
    except Exception:
        raise ArgonLogError('Unknown Error')


def recordmodule(func):
    def wrapper(*args):
        if len(args) == 2:
            modulelog(args[-1])
        else:
            modulelog('Unnamed Module')
        func(*args)
    return wrapper


def recordinfo(func):
    def wrapper(*args):
        status = func(*args)
        if len(args) == 2:
            matchlog(status, args[-1])
        else:
            matchlog(status, 'Unnamed Infomation')
    return wrapper


def recordopen(func):
    def wrapper(*args):
        modulelog('Connect Device')
        status = func(*args)
        matchlog(status, 'Open ' + args[-1])
    return wrapper


def recordclose(func):
    def wrapper(*args):
        modulelog('Disconnect Device')
        status = func(*args)
        matchlog(status, 'Close Port')
    return wrapper


def recordreset(func):
    def wrapper(*args):
        atr, status = func(*args)
        if status == 'Pass':
            matchlog(status, 'ATR:' + atr)
        elif status == 'Fail':
            matchlog(status, 'Reconnect Error')
        else:
            raise ArgonLogError('Unkown Status-ATR')
    return wrapper


def recordapdu(func):
    def wrapper(*args, **kwargs):
        rtn_data, rtn_sw, status = func(*args, **kwargs)

        # args存储APDU和msg(有默认值)
        if len(args) == 3:
            msg = args[-1]
        else:
            msg = 'Unnamed Command'

        # kwargs存储SW(单字符串/列表)和expectData
        if 'expect_data' in kwargs.keys():
            expect_data = kwargs['expect_data']
        else:
            expect_data = ''

        if 'sw' in kwargs.keys():
            expect_sw = kwargs['sw']
        else:
            expect_sw = ''

        # TODO 加入61XX和6CXX的情况
        if rtn_sw[:2] == '61':
            # 修改原始指令参数，去掉期望sw和resp
            apdu = '00C00000'+rtn_sw[2:]
            newmsg = 'Get Response'
            new_rtn_data, new_rtn_sw, status = func(args[0], apdu, newmsg, expect_data=expect_data, sw=expect_sw)

            matchlog(status, msg, args[1], rtn_data, '', rtn_sw, '')
            matchlog(status, newmsg, apdu, new_rtn_data, expect_data, new_rtn_sw, expect_sw)
        elif rtn_sw[:2] == '6C':
            # 修改原始指令参数，去掉期望sw和resp
            apdu = args[1][:-2] + rtn_sw[2:]
            newmsg = 'Resend Cmd'
            new_rtn_data, new_rtn_sw, status = func(args[0], apdu, newmsg, expect_data=expect_data, sw=expect_sw)

            matchlog(status, msg, args[1], rtn_data, '', rtn_sw, '')
            matchlog(status, newmsg, apdu, new_rtn_data, expect_data, new_rtn_sw, expect_sw)
        else:
            matchlog(status, msg, args[1], rtn_data, expect_data, rtn_sw, expect_sw)

    return wrapper


def recordmatch(func):
    def wrapper(*args):
        status = func(*args)
        if len(args) == 3:
            msg = args[-1]
        else:
            msg = 'Unnamed Match'

        matchlog(status, msg, args[0], args[1])
    return wrapper


def recorderror(func):
    def wrapper(*args):
        translog(label_error, args[-1])
        func(*args)
    return wrapper


def recordfail(func):
    def wrapper(*args):
        translog(label_fail, args[-1])
        func(*args)
    return wrapper


if __name__ == '__main__':
    initlog('Standard Process Testing')
    translog('Transcation First')
    modulelog('Select Application')
    matchlog('Pass',
             'Select Cmd',
             '00A4040008A000000333010101',
             '6F0A8408A000000333010101',
             '6F0A8408A000000333010101',
             '9000',
             '9000')

    matchlog('Fail',
             'Verify Cmd',
             '0020000000',
             '',
             '',
             '9000',
             '6C32')

    matchlog('Fail',
             'Compare Tag',
             '123456',
             '654321')
    matchlog('Pass', 'Check All Tags')
    matchlog('Info', 'Info Test')
    matchlog('Pass', 'Warning Test', 'Warning Test', 'Warning Test', 'Warning Test')
    # matchlog('Error', 'Error Test')

    modulelog('Application Init')
    matchlog('Warning', 'Warning Test')
    translog('Transcation Second')
    modulelog('GPO Cmd')
    modulelog('Compare AIP')
    modulelog('Compare AFL')
    translog('Transcation Third')
    translog('Summary')

    print(log_all)
    savecaselog()
