
import hashlib
import pyDHE
import time
import random
from lib.key import key,sessionkey
from lib.rsacrypto import rsacrypto

class message():
    """
        产生用来认证的传输信息, SYN, ACK
    """
    __MAX = 12322145625621452524554561

    def __init__(self):
        pass

    def syn(self):
        """
            Epub(A,B,ra,hash(Ra),T),Ra,sign(mac(A,B,ra,hash(Ra),T))
            return:  bytes
        """
        A = key().serve_public_key()
        B = key().client_public_key()
        ra = random.randint(0,self.__MAX)
        Ra_save = pyDHE.new()
        Ra = Ra_save.getPublicKey()
        Ra_md5 = hashlib.md5(str(Ra).encode()).hexdigest()
        T = int(time.time())

        message = F"{A}+{B}+{ra}+{Ra_md5}+{T}"
        message_encrypto = rsacrypto().serve_encrypt(message)
        sign = rsacrypto().client_sign(message)
        Ra = str(Ra).encode()

        content = message_encrypto + b'&&&' + Ra + b'&&&' + sign
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>syn  send !!!!!")
        return (content,Ra_save)


    def deal_syn(self, content):
        """
            服务端A对收到的syn数据进行处理,返回syn_ack需要的数据
        """
        global sessionkey
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>deal   syn  !!!!!")
        content_encrypto, Ra, sign = content.split(b'&&&')
        Ra = int(Ra.decode())
        #解密content
        content = rsacrypto().serve_decrypt(content_encrypto)
        #验证签名
        verify = rsacrypto().rsa_verify(content, sign, key().client_public_key())
        print("签名验证结果：",verify)
        A, B, ra, Ra_md5, T = content.split("+")
        T = int(T) + 1

        #生成rb, Rb
        rb = random.randint(0,self.__MAX)
        Rb_save = pyDHE.new()
        Rb = Rb_save.getPublicKey()
        sessionkey = sessionkey().serve_sessionkey(Ra, Rb_save)
        print("会话密钥：", sessionkey)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>deal syn success!!!!!")
        msg = [ra,rb, Rb, Rb_save,T]
        return msg


    def syn_ack(self, msg):
        """
            Epub(B,A,ra,rb,hash(Rb),T), Rb, sign(mac(B,A,ra,rb,hash(Rb),T))
        """
        ra, rb, Rb, Rb_save, T = msg
        A = key().serve_public_key()
        B = key().client_public_key()
        Rb_md5 = hashlib.md5(str(Rb).encode()).hexdigest()

        message = F"{B}+{A}+{ra}+{rb}+{Rb_md5}+{T}"
        message_encrypto = rsacrypto().client_encrypt(message)
        sign = rsacrypto().serve_sign(message)
        Rb = str(Rb).encode()

        content = message_encrypto + b'&&&' + Rb + b'&&&' + sign

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>syn_ack send success!!!!!")
        return content

    def deal_syn_ack(self, content, Ra):
        """
            客户端B对收到的syn_ack数据进行处理,返回ck需要的数据
        """
        global sessionkey
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>deal  syn_ack !!!!!")

        content_encrypto, Rb, sign = content.split(b'&&&')
        Rb = int(Rb.decode())
        #解密content
        content = rsacrypto().client_decrypt(content_encrypto)
        #验证签名
        verify = rsacrypto().rsa_verify(content, sign, key().serve_public_key())
        B, A, ra, rb, Rb_md5, T = content.split("+")
        T = int(T) + 1

        print("签名验证结果：", verify)
        
        sessionkey = sessionkey().client_sessionkey(Ra, Rb)
        print("会话密钥：", sessionkey)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>deal  syn_ack success !!!!!")
        msg = [ra,rb, Rb, T]
        return msg

    def ack(self, msg):
        """
            Epub(A, B, rb, T),sign(mac(A, B, rb, T))
        """
        ra, rb, Rb, T = msg
        A = key().serve_public_key()
        B = key().client_public_key()


        message = F"{A}+{B}+{rb}+{T}"
        message_encrypto = rsacrypto().serve_encrypt(message)
        sign = rsacrypto().client_sign(message)

        content = message_encrypto + b'&&&' + sign

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ack send success !!!!!")
        return content

    def deal_ack(self, content, srb, ST):
        """
            服务端A对收到的ack数据进行处理,验证时间戳，验证签名，验证随机数
        """
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>deal  ack !!!!!")
        content_encrypto, sign = content.split(b'&&&')
        #解密content
        content = rsacrypto().serve_decrypt(content_encrypto)
        #验证签名
        verify = rsacrypto().rsa_verify(content, sign, key().client_public_key())
        A, B, crb, CT = content.split("+")
        ST = int(ST) + 1

        if (int(ST) == int(CT) and int(crb) == int(srb)):
            print("时间戳和随机数验证通过！！！")
        else:
            print(ST,CT,crb,srb)
        print("签名验证结果：", verify)

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>deal  syn_ack success !!!!!")

    def encrypto_msg(self, msg, pc, key):
        """
            对称加密会话,key是私钥用来签名
        """
        message_encrypto = pc.encrypt(msg)
        sign = rsacrypto().rsa_sign(msg, key)

        content = message_encrypto + b'&&&' + sign

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>加密成功 !!!!!")
        return content

    def deal_encrypto_msg(self, content, pc, key):
        """
            处理对称加密会话，key是公钥钥用来验证签名
        """
        content_encrypto, sign = content.split(b'&&&')
        #  解密content
        content = pc.decrypt(content_encrypto)
        #  验证签名
        verify = rsacrypto().rsa_verify(content, sign, key)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>验证结果：", verify)
        return content


    def fine(self):
        pass

    def deal_fine(self):
        pass

