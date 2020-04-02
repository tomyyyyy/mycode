import socket
import time
import rsa
import hashlib
import random
from lib.message import message
from lib.banner import banner
from lib.key import sessionkey, key
from lib.aescrypto import prpcrypt


if __name__ == "__main__":

    banner().serve_banner()

    # 明确配置变量
    ip_port = ('127.0.0.1',8090)
    connect_amount = 5
    buffer_size = 102400

    # 创建一个TCP套接字
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
    ser.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # 对socket的配置重用ip和端口号
    # 绑定端口号
    ser.bind(ip_port)
    # 设置半连接池,最多可以连接多少个客户端
    ser.listen(connect_amount)   

    while 1:
        # 阻塞等待，创建连接
        con, address = ser.accept()       #在这个位置进行等待，监听端口号 
        
        #获得消息
        content = con.recv(buffer_size)
        # print("收到的消息：",content)
        #处理syn
        mssg = message().deal_syn(content)
        ra, rb, Rb, Rb_save, T = mssg
        #发送syn_ack
        content = message().syn_ack(mssg)
        # print("发送的消息：",content)
        con.send(content)
        content = con.recv(buffer_size)
        message().deal_ack(content, rb, T)

        sessionkey = sessionkey().get_serve_sessionkey()
        pc = prpcrypt(str(sessionkey)[0:16])

        print("======================验证通过==================")

        while 1:
            try:
                msg = con.recv(buffer_size)        #接受套接字的大小，怎么发就怎么收
                msg = message().deal_encrypto_msg(msg, pc, key().client_public_key())
                if msg == 'q':
                    con.close()
                print('服务器收到消息',msg)
                msg = input('please input:')
                # 防止输入空消息
                if not msg:
                    continue
                con.send(message().encrypto_msg(msg, pc, key().serve_private_key()))   # 收发消息一定要二进制，记得编码
                if msg == 'q':
                    break
            except Exception as e:
                break

    # 关闭服务器
    ser.close()

