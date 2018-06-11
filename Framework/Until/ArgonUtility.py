from ArgonLog import *


@recordmatch
def matchdata(data, expectdata, msg=''):
    if data != expectdata:
        status = 'Fail'
    else:
        status = 'Pass'
    return status


# 16进制转换成二进制
# def hextobin(str):
def hextobin(data):
    b = bin(int(data, 16))
    # 将字符串中的0b给去掉
    btmp = b.strip('0b')
    # 扩充字节的长度，如输入的数据是0F,期望返回的数据是00001111
    n = len(data)
    n1 = n*4
    result = btmp.zfill(n1)
    return result


# 二进制转换成十六进制
def bintohex(data):
    b = hex(int(data, 2))
    # 将字符串中的0b给去掉
    btmp = b.strip('0x')
    # 扩充字节的长度，如输入的数据是000000001100,期望返回的数据是00C
    n = len(data)
    n1 = int(n/4)
    result = btmp.zfill(n1)
    return result.upper()


# 字符串的比较
def strcmp(s1, s2):
    return (s1 > s2) - (s1 < s2)


# 字符串转换成ASCII码
def strtoascii(data):
    tmp = [ord(tmp1) for tmp1 in data]
    for i in range(0, tmp.__len__()):
        # 十进制转换成16进制
        tmp[i] = hex(tmp[i]).lstrip('0x')
    result = ''.join(tmp)
    return result.upper()


# ASCII转换成字符串
def asciitostr(data):
    result = ''
    n = int(data.__len__() / 2)
    for i in range(0, n):
        # 将十六进制转换成十进制
        tmp = int(data[2 * i:2 * i + 2], 16)
        tmp1 = chr(tmp)
        result += tmp1
    return result.upper()


# 十六进制字符串返回string型长度
def strlength(data):
    ilen = int(len(data) / 2)
    return bytes((ilen,)).hex().upper()


# 返回增加长度的十六进制字符串
def addlength(data):
    return strlength(data) + data


# 十六进制字符串返回int型长度
def intlength(data):
    return int(data, 16) * 2





















