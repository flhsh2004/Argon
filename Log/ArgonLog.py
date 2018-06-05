import yaml

# 存储单个脚本的日志内容
log_all = []
# 存储单个脚本的状态
casepass = True
# 单个脚本名称
casename = ''

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


class ArgonLogError(Exception):
    """日志保存处理类"""
    pass


def initlog(name):
    """初始化log存储名"""
    global casename
    casename = name


def savecaselog():
    """保存log并清空临时变量"""
    global casename
    global casepass
    try:
        stream = open(r'../LogDir/' + casename + '.yml', 'w')
        yaml.dump(log_all, stream)
        stream.close()
    except:
        raise Exception('Log Save Error')
    finally:
        casestatus = casepass

        log_all.clear()
        casename = ''
        casepass = True
        return casestatus


def translog(status, msg=''):
    """交易日志"""
    try:
        log_all.append({'level': level_trans,
                        'status': status,
                        'msg': msg,
                        'module': []})
    except:
        raise ArgonLogError('No Log Root')


def modulelog(msg=''):
    """模块日志"""
    try:
        log_trans = log_all[-1]
    except:
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
    except:
        raise ArgonLogError('No Trans Node')

    # 判断是否含有Module节点
    try:
        log_module = log_trans['module'][-1]
    except:
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
        # ADPU节点
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
    except:
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
        status = func(*args)
        modulelog('Connect Device')
        matchlog(status, 'Open' + args[-1])
    return wrapper


def recordclose(func):
    def wrapper(*args):
        status = func(*args)
        modulelog('Disconnect Device')
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
        RtnData, rtn, status = func(*args, **kwargs)

        # args存储APDU和msg(有默认值)
        if len(args) == 3:
            msg = args[-1]
        else:
            msg = 'Unnamed Command'

        # kwargs存储SW(单字符串/列表)和expectData
        if 'expectData' in kwargs.keys():
            expectData = kwargs['expectData']
        else:
            expectData = ''

        if 'SW' in kwargs.keys():
            SW = kwargs['SW']
        else:
            SW = ''

        matchlog(status, msg, args[1], RtnData, expectData, rtn, SW)
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