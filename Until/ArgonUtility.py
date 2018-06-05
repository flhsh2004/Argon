    #16进制转换成二进制
    #def hextobin(str):
def hextobin(str):
    result = ''
    b=bin(int(str,16))
    #将字符串中的0b给去掉
    btmp =b.strip('0b')
    #扩充字节的长度，如输入的数据是0F,期望返回的数据是00001111
    n=len(str)
    n1=n*4
    result=btmp.zfill(n1)
    return result

#二进制转换成十六进制
def bintohex(str):
    result = ''
    b=hex(int(str,2))
    # 将字符串中的0b给去掉
    btmp = b.strip('0x')
    # 扩充字节的长度，如输入的数据是000000001100,期望返回的数据是00C
    n = len(str)
    n1 = int(n/4)
    result = btmp.zfill(n1)
    return result.upper()

#字符串的比较
def strcmp(s1,s2):
    return (s1>s2)-(s1<s2)

#字符串转换成ASCII码
def strtoascii(str):
    result = ''
    tmp = [ord(tmp1) for tmp1 in str]
    for i in range(0, tmp.__len__()):
        # 十进制转换成16进制
        tmp[i]=hex(tmp[i]).lstrip('0x')
    result = ''.join(tmp)
    return result.upper()

#ASCII转换成字符串
def asciitostr(str):
    result=''
    n=int(str.__len__() / 2)
    for i in range(0, n):
        #将十六进制转换成十进制
        tmp=int(str[2 * i:2 * i + 2], 16)
        tmp1=chr(tmp)
        result+=tmp1
    return result.upper()
























