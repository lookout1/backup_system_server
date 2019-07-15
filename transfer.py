#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os

BUFFSIZE=4096
ACK='OK\0'

def sendFile(s,sourceFilePath):

    fstat = os.stat(sourceFilePath)
    #发送文件长度
    s.sendall(str(fstat.st_size) + '\0')
    buf = s.recv(BUFFSIZE).strip('\0')

    fi = open(sourceFilePath, 'rb')
    length = fstat.st_size
    #读取文件内容并发送
    while (length > 0):
        buf = fi.read(BUFFSIZE)
        s.sendall(buf)
        length -= len(buf)
    fi.close()

    #等待确认
    buf = s.recv(BUFFSIZE).strip('\0')

def recvFile(s,sourceFilePath):
    #接收文件长度
    length=s.recv(BUFFSIZE).strip('\0')
    s.sendall(ACK)
    length=long(length)

    #接收文件
    fo=open(sourceFilePath,'wb')
    while(length>0):
        buf=s.recv(min(BUFFSIZE,length))
        fo.write(buf)
        length-=len(buf)
    fo.close()

    #发送确认
    s.sendall(ACK)