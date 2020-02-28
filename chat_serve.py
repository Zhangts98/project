"""
chat room
env:python3
socket and fork exercise
群聊聊天室
功能 ： 类似qq群功能
【1】 有人进入聊天室需要输入姓名，姓名不能重复
【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx
"""


from socket import *
import  os

#构建全局变量
ADDR=('0.0.0.0',8888)

# 应用于存储用户 {name:address}
user={}

# 处理进入聊天室请求
def do_login(s,name,addr):
    if name in user or "管理" in name:
        s.sendto(b'FAIL',addr)
        return
    else:
        s.sendto(b"OK", addr)

    # 通知其他人
    msg = "\n欢迎 '%s' 进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(), user[i])
    user[name] = addr  # 字典中加入一项

#处理聊天功能
def do_chat(s,name,content):
    msg = "\n%s : %s"%(name,content)
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])

#处理退出
def do_quit(s,name):
    msg="%s 退出聊天."%name
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    #删除用户
    del user[name]

#基本结构(接收请求,分配任务)
def main():
    #udp服务端套接字
    s=socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid =os.fork()
    if pid < 0:
        print('Error')
    elif pid == 0:
        # 子进程处理发送管理员消息
        while True:
            content=input("管理员消息:")
            msg='C %s %s'%("管理员消息",content)
            s.sendto(msg.encode(),ADDR)# 从子进程发送给了父进程
    else:
        #循环接收请求
        while True:
            data,addr=s.recvfrom(1024)
            tmp=data.decode().split(' ',2)# 请求内容做简单的解析
            #print("接收到的请求: ",tmp)
            #data-->收到的请求
            if tmp[0]=='L':
                do_login(s,tmp[1],addr)
            elif tmp[0]=='C':
                # tmp=[C NAME XXXX]
                do_chat(s,tmp[1],tmp[2])
            elif tmp[0]=='Q':
                do_quit(s,tmp[1])

if __name__=='__main__':
    main()


