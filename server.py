#!/usr/bin/python
# -*- coding:UTF-8 -*-
import SocketServer,transfer,os

HOST=''
PORT=12345
ADDR=(HOST,PORT)
BUFFSIZE=4096
ACK='OK\0'
ROOT='./backup/'  #服务器存储备份文件的目录

def main():
    tcpServ = SocketServer.ThreadingTCPServer(ADDR, requestHandler)
    print 'waiting for connection...'
    tcpServ.serve_forever()

def backup(s):
    #接收文件路径
    filePath=s.recv(BUFFSIZE).strip('\0')
    s.sendall(ACK)

    #接收文件
    transfer.recvFile(s,ROOT+filePath)


def restore(s):
    # 接收文件路径
    filePath = s.recv(BUFFSIZE).strip('\0')
    s.sendall(ACK)

    # 发送文件
    transfer.sendFile(s,ROOT+filePath)

def delete(s):
    # 接收文件路径
    filePath = s.recv(BUFFSIZE).strip('\0')

    # 删除文件
    os.remove(ROOT+filePath)

    s.sendall(ACK)

class requestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print '...connected from:',self.client_address
        #接收命令
        buf=self.request.recv(BUFFSIZE).strip('\0')
        if buf=='backup':
            #发送命令确认
            self.request.sendall(ACK)
            backup(self.request)
        elif buf=='restore':
            #发送命令确认
            self.request.sendall(ACK)
            restore(self.request)
        elif buf =='delete':
            #发送命令确认
            self.request.sendall(ACK)
            delete(self.request)
        else:
            pass


main()
