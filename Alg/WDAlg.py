#!/usr/bin/python
# -*- coding: utf-8 -*-
# 需要安装 PyCryptodome模块
import hashlib
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import MD5, SHA1, SHA256, SHA384, SHA512
from ctypes import *
from binascii import *
from ArgonUtility import *
import ctypes

class wdalgerr(ValueError):  #继承ValueError，此类在Crypto模块中实现
    pass

# HASH算法
#计算SHA1
def sha1(str):
    result = ''
    hash = hashlib.sha1()
    hash.update(bytes.fromhex(str))
    result = hash.hexdigest()
    return result

#计算SHA256
def sha256(str):
    result = ''
    hash = hashlib.sha256()
    hash.update(bytes.fromhex(str))
    result = hash.hexdigest()
    return result

#计算MD5
def md5(str):
    result = ''
    hash = hashlib.md5()
    hash.update(bytes.fromhex(str))
    result = hash.hexdigest()
    return result

#计算SHA384
def sha384(str):
    result = ''
    hash = hashlib.sha384()
    hash.update(bytes.fromhex(str))
    result = hash.hexdigest()
    return result

#计算SHA512
def sha512(str):
    result = ''
    hash = hashlib.sha512()
    hash.update(bytes.fromhex(str))
    result = hash.hexdigest()
    return result

#AES算法的ECB模式的加密解密
def AESECB(data, protectKey, type):
    if (len(protectKey)/2) % 16 != 0:
        raise wdalgerr("Incorrect AES key length (%d bytes)" % (len(protectKey)/2))
    if (len(data)/2) % 16 != 0:
        data = data + "80"
        while (len(data)/2) % 16 != 0:
            data += "00"
            if (len(data)/2) % 16 == 0:
                break
    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    result = ''
    if type == 1:  #加密
        aes = AES.new(Keybytes, AES.MODE_ECB)
        endata = aes.encrypt(databytes)
        result = endata.hex()

    if type == 2:  #解密
        aes = AES.new(Keybytes, AES.MODE_ECB)
        dedata = aes.decrypt(databytes)
        result = dedata.hex()

    return result

#AES算法的CBC模式的加密解密
def AESCBC(data, protectKey, type, iv):
    if (len(protectKey)/2) % 16 != 0:
        raise wdalgerr("Incorrect AES key length (%d bytes)" % (len(protectKey)/2))
    if (len(iv)/2) % 16 != 0:
        raise wdalgerr("Incorrect AES iv  length (%d bytes)" % (len(iv)/2))
    if (len(data)/2) % 16 != 0:
        data = data + "80"
        while (len(data)/2) % 16 != 0:
            data += "00"
            if (len(data)/2) % 16 == 0:
                break
    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    ivbytes = bytes.fromhex(iv)
    result = ''
    if type == 1:  #加密
        aes = AES.new(Keybytes, AES.MODE_CBC, ivbytes)
        endata = aes.encrypt(databytes)
        result = endata.hex()

    if type == 2:  #解密
        aes = AES.new(Keybytes, AES.MODE_CBC, ivbytes)
        dedata = aes.decrypt(databytes)
        result = dedata.hex()
    return result


#DES算法的ECB模式的加密解密
def DESECB(data, protectKey, type):
    if (len(protectKey)/2) % 8 != 0:
        raise wdalgerr("Incorrect des key length (%d bytes)" % (len(protectKey)/2))
    if (len(data)/2) % 8 != 0:
        data = data + "80"
        while (len(data)/2) % 8 != 0:
            data += "00"
            if (len(data)/2) % 8 == 0:
                break

    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    result = ''
    if type == 1:  #加密
        des = DES.new(Keybytes, DES.MODE_ECB)
        endata = des.encrypt(databytes)
        print(endata)
        result = endata.hex()
    if type == 2:  #解密
        des = DES.new(Keybytes, DES.MODE_ECB)
        dedata = des.decrypt(databytes)
        result = dedata.hex()
    return result

#DES算法的CBC模式的加密解密
def DESCBC(data, protectKey, type, iv):
    if (len(protectKey)/2) % 8 != 0:
        raise wdalgerr("Incorrect des key length (%d bytes)" % (len(protectKey)/2))
    if (len(iv)/2) % 8 != 0:
        raise wdalgerr("Incorrect des iv  length (%d bytes)" % (len(iv)/2))
    if (len(data)/2) % 8 != 0:
        data = data + "80"
        while (len(data)/2) % 8 != 0:
            data += "00"
            if (len(data)/2) % 8 == 0:
                break
    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    ivbytes = bytes.fromhex(iv)
    result = ''
    if type == 1:  #加密
        des = DES.new(Keybytes, DES.MODE_CBC, ivbytes)
        endata = des.encrypt(databytes)
        result = endata.hex()
    if type == 2:  #解密
        des = DES.new(Keybytes, DES.MODE_CBC, ivbytes)
        dedata = des.decrypt(databytes)
        result = dedata.hex()
    return result

#3DES算法的ECB模式的加密解密
def DES3ECB(data, protectKey, type):
    if (len(protectKey)/2) % 16 != 0:
        raise wdalgerr("Incorrect 3des key length (%d bytes)" % (len(protectKey)/2))
    if protectKey[:16] == protectKey[16:32] or protectKey[-32:-16] == protectKey[-16:]:
        raise wdalgerr("Triple DES key degenerates to single DES")

    if (len(data)/2) % 8 != 0:
        data = data + "80"
        while (len(data)/2) % 8 != 0:
            data += "00"
            if (len(data)/2) % 8 == 0:
                break
    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    result = ''
    if type == 1:  #加密
        des = DES3.new(Keybytes, DES.MODE_ECB)
        endata = des.encrypt(databytes)
        result = endata.hex()
    if type == 2:  #解密
        des = DES3.new(Keybytes, DES.MODE_ECB)
        dedata = des.decrypt(databytes)
        result = dedata.hex()
    return result

#3DES算法的CBC模式的加密解密
def DES3CBC(data, protectKey, type, iv):
    if (len(protectKey)/2) % 16 != 0:
        raise wdalgerr("Incorrect 3des key length (%d bytes)" % (len(protectKey)/2))
    if (len(iv)/2) % 16 != 0:
        raise wdalgerr("Incorrect 3des iv length (%d bytes)" % (len(iv)/2))
    if protectKey[:16] == protectKey[16:32] or protectKey[-32:-16] == protectKey[-16:]:
        raise wdalgerr("Triple DES key degenerates to single DES")
    if (len(data)/2) % 8 != 0:
        data = data + "80"
        while (len(data)/2) % 8 != 0:
            data += "00"
            if (len(data)/2) % 8 == 0:
                break
    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    ivbytes = bytes.fromhex(iv)
    result = ''
    if type == 1:  #加密
        des = DES3.new(Keybytes, DES.MODE_CBC, ivbytes)
        endata = des.encrypt(databytes)
        result = endata.hex()
    if type == 2:  #解密
        des = DES3.new(Keybytes, DES.MODE_CBC, ivbytes)
        dedata = des.decrypt(databytes)
        result = dedata.hex()
    return result

#字符串进行异或
def stringxor(str1,str2):
    orxstr=""
    for i in range(0,len(str1)):
        val1 = int(list(str1)[i],16)
        val2 = int(list(str2)[i],16)
        rst = str(hex(val1^val2))
        rst = rst[2]
        orxstr = orxstr+rst
    return orxstr

#字符串取反
def stringnot(str):
    orxstr=""
    for i in range(0, len(str)):
        vall1 = int(list(str)[i], 16)
        rst = (~vall1) & 0x0f
        rst = hex(rst)
        rst = rst[2]
        orxstr = orxstr + rst
    return orxstr

#3DES计算MAC
def DES3MAC(data, protectKey,iv,maclen):
    if (len(protectKey)/2) % 16 != 0:
        raise wdalgerr("Incorrect 3des key length (%d bytes)" % (len(protectKey)/2))
    if (len(iv)/2) % 8 != 0:
        raise wdalgerr("Incorrect 3des iv length (%d bytes)" % (len(iv)/2))
    if protectKey[:16] == protectKey[16:32] or protectKey[-32:-16] == protectKey[-16:]:
        raise wdalgerr("Triple DES key degenerates to single DES")
    if (len(data) / 2) % 8 == 0:  #最后一包为8字节，则补
        data = data + "8000000000000000"
    if (len(data)/2) % 8 != 0:   #最后一包不为8字节，则补8000至8字节
        data = data + "80"
        while (len(data)/2) % 8 != 0:
            data += "00"
            if (len(data)/2) % 8 == 0:
                break

    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    ivbytes = bytes.fromhex(iv)
    des = DES3.new(Keybytes, DES.MODE_CBC, ivbytes)
    endata = des.encrypt(databytes)
    strendata = endata.hex()
    strdata = strendata[-16:]
    desmac = strdata[:2*maclen]
    return desmac

#DES计算MAC
def DESMAC(data, protectKey, iv, maclen):
    if (len(protectKey)/2) % 8 != 0:
        raise wdalgerr("Incorrect des key length (%d bytes)" % (len(protectKey)/2))
    if (len(iv)/2) % 8 != 0:
        raise wdalgerr("Incorrect des iv length (%d bytes)" % (len(iv)/2))
    if (len(data) / 2) % 8 == 0:  # 最后一包为8字节，则补
        data = data + "8000000000000000"
        data = data + "80"
        while (len(data) / 2) % 8 != 0:
            data += "00"
            if (len(data) / 2) % 8 == 0:
                break

    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    ivbytes = bytes.fromhex(iv)
    des = DES.new(Keybytes, DES.MODE_CBC, ivbytes)
    endata = des.encrypt(databytes)
    strendata = endata.hex()
    strdata = strendata[-16:]
    desmac = strdata[:2 * maclen]
    return desmac


#3DES计算MAC
def AESMAC(data, protectKey,iv,maclen):
    if (len(protectKey)/2) % 16 != 0:
        raise wdalgerr("Incorrect AES key length (%d bytes)" % (len(protectKey)/2))
    if (len(iv)/2) % 16 != 0:
        raise wdalgerr("Incorrect AES iv length (%d bytes)" % (len(iv)/2))
    if (len(data) / 2) % 16 == 0:  #最后一包为8字节，则补
        data = data + "8000000000000000"
    if (len(data)/2) % 16 != 0:   #最后一包不为8字节，则补8000至8字节
        data = data + "80"
        while (len(data)/2) % 16 != 0:
            data += "00"
            if (len(data)/2) % 16 == 0:
                break

    databytes = bytes.fromhex(data)
    Keybytes = bytes.fromhex(protectKey)
    ivbytes = bytes.fromhex(iv)
    aes = AES.new(Keybytes, AES.MODE_CBC, ivbytes)
    endata = aes.encrypt(databytes)
    strendata = endata.hex()
    strdata = strendata[-32:]
    aesmac = strdata[:2*maclen]
    return aesmac


#RSA算法公钥加密
def RSAencryptPublic(data,n,e="010001"):
    RsaID = "300d06092a864886f70d0101010500" #RSA的算法标识
    if len(n)/2 ==128: #rsa1024
        if n[0:2] > "80":
            pubkey = "00" + n
            publickey ="30819f"+ RsaID+"03818d00308189028181"+pubkey+"0203"+e

        if n[0:2] < "80":
           publickey ="30819e"+ RsaID+"03818c00308188028180"+n+"0203"+e

    if len(n) / 2 == 256:  # rsa2048
        if n[0:2] > "80":
            pubkey = "00" + n
            publickey ="30820122"+ RsaID+"0382010f003082010a02820101"+pubkey+"0203"+e

        if n[0:2] < "80":
           publickey ="30820121"+ RsaID+"0382010e003082010902820100"+n+"0203"+e

    public_keyBytes = bytes.fromhex(publickey)
    public = RSA.importKey(public_keyBytes)  # 导入读取到的公钥
    enchiper = Cipher_pkcs1_v1_5.new(public)  # 生成对象
    endata = enchiper.encrypt(a2b_hex(data))
    result = endata.hex()
    return result


# RSA算法公钥验签
def RSAverifyPublic(data,signdata,n,h,e="010001"):
    RsaID = "300d06092a864886f70d0101010500" #RSA的算法标识
    if len(n)/2 ==128: #rsa1024
        if n[0:2] > "80":
            pubkey = "00" + n
            publickey ="30819f"+ RsaID+"03818d00308189028181"+pubkey+"0203"+e

        if n[0:2] < "80":
           publickey ="30819e"+ RsaID+"03818c00308188028180"+n+"0203"+e

    if len(n) / 2 == 256:  # rsa2048
        if n[0:2] > "80":
            pubkey = "00" + n
            publickey ="30820122"+ RsaID+"0382010f003082010a02820101"+pubkey+"0203"+e

        if n[0:2] < "80":
           publickey ="30820121"+ RsaID+"0382010e003082010902820100"+n+"0203"+e

    public_keyBytes = bytes.fromhex(publickey)
    public = RSA.importKey(public_keyBytes)  # 导入读取到的公钥
    verifier = PKCS1_v1_5.new(public)  # 生成对象
    if h == "MD5":
        verdata = verifier.verify(MD5.new(a2b_hex(data)), a2b_hex(signdata))
    if h == "SHA1":
        verdata = verifier.verify(SHA1.new(a2b_hex(data)), a2b_hex(signdata))
    if h == "SHA256":
        verdata = verifier.verify(SHA256.new(a2b_hex(data)), a2b_hex(signdata))
    if h == "SHA384":
        verdata = verifier.verify(SHA384.new(a2b_hex(data)), a2b_hex(signdata))
    if h == "SHA512":
        verdata = verifier.verify(SHA512.new(a2b_hex(data)), a2b_hex(signdata))
    return verdata

#公钥运算
def RSApubilc(data,n,e):
    if (len(n)/2) % 128 != 0 :
        raise ValueError("Incorrect RSA pubilc key length (%d bytes)" % (len(n)/2))
    dlla = windll.LoadLibrary("RSA.dll")
    # 参数1：data转换n
    data1 = c_char_p(data.encode("utf8"))
    # 参数2：公钥n转换
    n1 = c_char_p(n.encode("utf8"))
    # 参数3：公钥e转换
    e1 = c_char_p(e.encode("utf8"))
    #参数4：outdata
    if len(n) / 2 == 128:  # rsa1024
        outdata = create_string_buffer(256)
    if len(n) / 2 == 256:  # rsa1024
        outdata = create_string_buffer(512)

    #调动态库的接口
    result = dlla.RSAPublic(n1, e1, data1, outdata)

    if result == 0:
        print("公钥运算失败")
        return False
    else:
        print("公钥运算成功")
        return outdata.raw


# 私钥运算
def RSAPrivate(data,n,d):
    if (len(n)/2) % 128 != 0 :
        raise ValueError("Incorrect RSA pubilc key length (%d bytes)" % (len(n)/2))
    if (len()/2) % 128 != 0 :
        raise ValueError("Incorrect RSA Private key length (%d bytes)" % (len(n)/2))
    dlla = windll.LoadLibrary("RSA.dll")
    # 参数1：data转换
    data1 = c_char_p(data.encode("utf8"))
    # 参数2：公钥n转换
    n1 = c_char_p(n.encode("utf8"))
    # 参数3：公钥e转换
    d1 = c_char_p(d.encode("utf8"))
    # 参数4：outdata
    if len(n) / 2 == 128:  # rsa1024
        outdata = create_string_buffer(256)
    if len(n) / 2 == 256:  # rsa1024
        outdata = create_string_buffer(512)

    #调动态库的接口
    result = dlla.RSAPublic(n1, d1, data1, outdata)

    if result == 0:
        print("私钥运算失败")
        return False
    else:
        print("私钥运算成功")
        return outdata.raw


# 使用CRT格式进行私钥运算
def RSAPrivateCRT(data, p, q, dp, dq, Qinv):
    dlla = windll.LoadLibrary("RSA.dll")
    # 参数1：data转换
    data1 = c_char_p(data.encode("utf8"))
    # 参数2：p转换
    p1 = c_char_p(p.encode("utf8"))
    # 参数3：q转换
    q1 = c_char_p(q.encode("utf8"))
    # 参数4：dp转换
    dp1 = c_char_p(dp.encode("utf8"))
    # 参数5：dq转换
    dq1 = c_char_p(dq.encode("utf8"))
    # 参数6：Qinv转换
    Qinv1 = c_char_p(Qinv.encode("utf8"))

    #参数4：outdata
    if len(p) / 2 == 64:  # rsa1024
        outdata = create_string_buffer(256)
    if len(p) / 2 == 128:  # rsa1024
        outdata = create_string_buffer(512)

    #调动态库的接口
    #result = dlla.RSAPrivateCRT(data1, p1, q1, dp1, dq1, Qinv1, outdata)
    try:
        result = dlla.RSAPrivateCRT(p1, q1, dp1, dq1, Qinv1,data1, outdata)
        print(outdata.raw)
    except Exception as e:
        print("test")
        print(e)

    if result == 0:
        print("私钥运算失败")
        return False
    else:
        print("私钥运算成功")
        return outdata.raw


if __name__ == '__main__':
    a = AESMAC("1122334455667788", "112233445566778811223344556677", "00000000000000000000000000000000",4)
    print(a)
    a = RSAPrivateCRT(
        "6F4BB144FA1FBFD43B9C9D760B943648FDC0711E1244745083BE7C3D8A9396B30640D8F3758AD7ABF04CA1B9FDE3FD107DD3482814B07421D60F0732101AD07B653B53F9550E5990448C93823109D41E8E0C6CFF0B1CC706C1C9B3D5537E7D3F332AA3F766DC42633E4C3512E37FA1E21A4919C73F0D5B04340282DB18A93F09",
        "FAE4FCEF8FECEDDC44167746995DC3CCF6B1A2357B5B7726EFAB0BC3038916EAD7AC70CAB079EB7E584EA95F3B439FF32C896CC02D6CE999EA7D3C43CCF1991F",
        "C72311671557DCF6ABAA10E1EA439D70606B339CBEED34D3114BEEB614ED2A26DA7DD6A6FFD177EC7321D9C7D1D36F5C12B46D6B28ADF56694A10314539B9B11",
        "C815E02588E951944CF481B0DAD46D374331CC83CC59D83F43F96BCADD41F1F5DD8416FB7E1BED1378875B09A870B8D9AC95F81596E479B396CEC345EAE66DCF",
        "B373449172485554EC693B017A8C27EA46D9140FA2763BEE205E1EE572822E44090CF14C58A7B8BC191C5E16955D45B2E1203AA2206C730257D9A8DEBE613121",
        "0182A6D3F0C7447DCD762ED09A95ACE4CEB9B71E5CB18EF276E590D8931C4B46BBB9F508279DBDA0CB3147A634C8A3E56A825CC2606F946AF48A3D9BEF6DA4FB")
    print(a)
    '''
    a = RSApubilc(
        "6F4BB144FA1FBFD43B9C9D760B943648FDC0711E1244745083BE7C3D8A9396B30640D8F3758AD7ABF04CA1B9FDE3FD107DD3482814B07421D60F0732101AD07B653B53F9550E5990448C93823109D41E8E0C6CFF0B1CC706C1C9B3D5537E7D3F332AA3F766DC42633E4C3512E37FA1E21A4919C73F0D5B04340282DB18A93F09",
        "D725FAC96E763D279E08BEF556DAEF4EA10B5B6EED157844D009CEF3DCED25C53B7E689829C002B05F8B631E75C3702BFF1246B08D31BC0E456789D099950A3335E69A428E299F95CF5F661241ACDA0D2EDD1513A32BD241B2F9A8AEE36D4EA0446217443EE39F924EE70374EFE0D6DCBD362BEC6355F29B94C9655F6D51145F",
        "010001")
    print(a)
    a = AESMAC("1122334455667788", "11223344556677881122334455667788", "00000000000000000000000000000000",4)
    print(a)
    a = DESMAC("1122334455667788", "112233445566778899", "0000000000000000",4)
    print(a)
 
    a =DES3MAC("112233", "11223344556677881122334455667799",  "11223344556677880000000000000000", 4)
    print(a)
    
    a = DES3CBC("112233", "11223344556677881122334455667799", 1, "1122334455667788112233445566778899")
    a = AESCBC("112233", "11223344556677881122334455667788", 1, "1122334455667788112233445566778899")
    a = AESECB("112233", "1122334455667788112233445566778899", 1)

    print(a)
    a = RSApubilc(
        "6F4BB144FA1FBFD43B9C9D760B943648FDC0711E1244745083BE7C3D8A9396B30640D8F3758AD7ABF04CA1B9FDE3FD107DD3482814B07421D60F0732101AD07B653B53F9550E5990448C93823109D41E8E0C6CFF0B1CC706C1C9B3D5537E7D3F332AA3F766DC42633E4C3512E37FA1E21A4919C73F0D5B04340282DB18A93F09",
        "25FAC96E763D279E08BEF556DAEF4EA10B5B6EED157844D009CEF3DCED25C53B7E689829C002B05F8B631E75C3702BFF1246B08D31BC0E456789D099950A3335E69A428E299F95CF5F661241ACDA0D2EDD1513A32BD241B2F9A8AEE36D4EA0446217443EE39F924EE70374EFE0D6DCBD362BEC6355F29B94C9655F6D51145F",
        "010001")
    print(a)


    a = RSApubilc(
        "112233445566FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF003021300906052B0E03021A050004141122334455667788990011223344556677889900",
        "AFBEB17D6D0313A2D09751986DB80073C77718FE10EE3E765B14A22B3BB4160D525BFE7945B916FC09A65555D524B3BF67AE270D95094E5C46D9EA0476C0BC2056F2712E7CA3A8FAB47E2521ECCDA8BD0C13E3E1D9AE516E3F5AF545940272D576223EB7351F1E861C78914747394ECC81B8E28BABD3CA44AAD0CEEB1214AFF5",
        "010001")
    print(a)

    a = RSApubilc(
        "25A52EB09681F8E2D911F9B57D328C3E0F1237C5BA156232B9F0310FFB864963CAAD4B519E05789ACA4BD748FDF58194112B797550739F6F7C997A99C30044A7EC84E05530D06AB091FE1E0BA52DC04294BDDB69C4589F72DB048FB35C5AFDF105838B6D9DD559E20FA40CAE93F459D5F855931C3CD244EA041664B3094BB3C745B536B918AEBAEBB4AC153B9B3D995BE90942A75A504E05679888BE40538D4CB32CADC9DABF52D906AFF0E77F755108878FD7DB5F77D47EF2832C26A004CE3DB25F00D71F05F657325C7503D6549056E35A07C89A9FE630CEC55C80B29582C3B99BCE676C7DAA27B10E046A227AA79796C1D0E6116CA14EF75A81CE3B877C94",
        "B2CB12E93A2063A6F95DA2430C93D554EB66D56A51E2EE3AD130EAE062B8AEFF3B0ED1E6A864F3D4C8E8FEA0AD07C0C5D6A3C049B7FAD9960A27D7886B4A74139956021A9D6C146A6BCB81157C26081D251C662E4C42BB959940AEE0B328C0FCDA97CCA8EF0AF4E6FC9C0E6CD01C64C6B7DBE47729FC8B93E5CDD011E0640FC19676B56BA8A2CD2A31C4DE63392C016AE512E8BB0A1179D1FA4A8A86A28285898EDCAB52377084DFB53C4D5E0F88ECA79CE3D2001927546A8C589B83CFEE603EEA7026199086C49CCB7DD70764164E1961DCF17E50748573FDDF457A2446F86B682EB91942A1975E126A34F4C42337BC7338216339E80627CAC0A96D5ED20AC5",
        "010001")
    print(a)

    a = RSAPrivate(
        "6F4BB144FA1FBFD43B9C9D760B943648FDC0711E1244745083BE7C3D8A9396B30640D8F3758AD7ABF04CA1B9FDE3FD107DD3482814B07421D60F0732101AD07B653B53F9550E5990448C93823109D41E8E0C6CFF0B1CC706C1C9B3D5537E7D3F332AA3F766DC42633E4C3512E37FA1E21A4919C73F0D5B04340282DB18A93F09",
        "C32A5EFB097A6C5C8809026A993D1167391717E160CBFF8FA5F0C6027553A9C7C0BD412B4C62A9E123BAAE911DEDA4839CF24069DA962E2CB4658B3AFDC73931D847181647440B696B791F2C531C9EE6DAABF1BBED545405C73158A56B63D7392DA5A68289A4C2EB18E9DBE7CA9BAED7030DAA9F61410713EE77CBEFA685F00F",
        "B509C3EB888248AC99000A7EC9C12D389C6BC09A2F896C7A5B0AFB12E2B5060426D527F3BB3AB6AD02D0B4082743FF5C9B24D8FD9867C15374CFD1149ABEC85CC3F61BDBE8B0F7BFDFEA7E2369BEBF9754535728350F36061E0E9CB6EF02374C4EAE45A4428A361DB540404522483917DE5B12D9E251B5D139744F076B9E2CE1")
    print(a)

    a = RSAPrivateCRT(
        "6F4BB144FA1FBFD43B9C9D760B943648FDC0711E1244745083BE7C3D8A9396B30640D8F3758AD7ABF04CA1B9FDE3FD107DD3482814B07421D60F0732101AD07B653B53F9550E5990448C93823109D41E8E0C6CFF0B1CC706C1C9B3D5537E7D3F332AA3F766DC42633E4C3512E37FA1E21A4919C73F0D5B04340282DB18A93F09",
        "FAE4FCEF8FECEDDC44167746995DC3CCF6B1A2357B5B7726EFAB0BC3038916EAD7AC70CAB079EB7E584EA95F3B439FF32C896CC02D6CE999EA7D3C43CCF1991F",
        "C72311671557DCF6ABAA10E1EA439D70606B339CBEED34D3114BEEB614ED2A26DA7DD6A6FFD177EC7321D9C7D1D36F5C12B46D6B28ADF56694A10314539B9B11",
        "C815E02588E951944CF481B0DAD46D374331CC83CC59D83F43F96BCADD41F1F5DD8416FB7E1BED1378875B09A870B8D9AC95F81596E479B396CEC345EAE66DCF",
        "B373449172485554EC693B017A8C27EA46D9140FA2763BEE205E1EE572822E44090CF14C58A7B8BC191C5E16955D45B2E1203AA2206C730257D9A8DEBE613121",
        "0182A6D3F0C7447DCD762ED09A95ACE4CEB9B71E5CB18EF276E590D8931C4B46BBB9F508279DBDA0CB3147A634C8A3E56A825CC2606F946AF48A3D9BEF6DA4FB")
    print(a)

'''

