"""
chat room客户端
发送请求,得到结果



"""

from socket import *
import os,sys

#服务器地址
ADDR=('192.168.0.107',8888)

#发送消息
def send_msg(s,name):
    while True:
        try:
            content=input("发言: ")
        except:
            content='quit'
        if content=='quit':
            msg='Q '+name
            s.sendto(msg.encode(),ADDR)
            sys.exit("谢谢使用!")
        msg='C %s %s '%(name,content)#根据协议组织消息
        s.sendto(msg.encode(),ADDR)


#接收消息
def recv_msg(s):
    while True:
        data,addr=s.recvfrom(1024)
        #该进程应该退出
        if data.decode()=='EXIT':
            sys.exit()
        print(data.decode()+'\n发言: ',end='')


#启动函数-->向服务端发送初始请求
def main():
    #udp客户端
    s=socket(AF_INET,SOCK_DGRAM)

    while True:
        name=input("请输入姓名: ")
        msg='L '+name# 组织协议的格式
        s.sendto(msg.encode(),ADDR)#发送请求
        data,addr=s.recvfrom(1024)#等待反馈结果
        if data.decode()=='OK':
            print("您已进入聊天室")
            break
        else:
            print("该用户已存在")

    #准备聊天
    # 创建父子进程
    pid=os.fork()
    if pid < 0:
        print("Error")
        return
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s)


if __name__=='__main__':
    main()