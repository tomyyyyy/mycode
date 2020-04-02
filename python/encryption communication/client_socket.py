import socket
import time
import random
import hashlib
import rsa
import base64
from lib.message import message
from lib.key import sessionkey, key
from lib.banner import banner
from lib.aescrypto import prpcrypt


def main():
    global sessionkey
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.connect(('127.0.0.1',8090))

    #发送syn
    content, Ra = message().syn()
    p.send(content)
    # print("发送的消息：", content)
    #获得消息,处理syn_ack
    msgg = p.recv(10240)
    mag = message().deal_syn_ack(msgg, Ra)
    # print("收到的消息：", mag)
    p.send(message().ack(mag))

    sessionkey = sessionkey().get_client_sessionkey()
    pc = prpcrypt(str(sessionkey)[0:16])

    print("======================验证通过==================")
    #检验参数
    while 1:
        msg = input('please input:')
        # 防止输入空消息
        if not msg:
            continue
        p.send(message().encrypto_msg(msg, pc, key().client_private_key()))   # 收发消息一定要二进制，记得编码
        if msg == 'q':
            break
        
        msg = p.recv(10240)        #接受套接字的大小，怎么发就怎么收
        msg = message().deal_encrypto_msg(msg, pc, key().serve_public_key())
        if msg == 'q':
            p.close()
        print('服务器收到消息',msg)
    p.close()


if __name__ == "__main__":
    banner().client_banner()
    main()