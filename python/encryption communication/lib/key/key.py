import rsa
import sys

class key():
    """
        该类是为了获得密钥所建立的，可以获得其中的密钥值
    """

    dir = "D:\\my code\\python密码学\\res\\pem\\"

    with open(dir+'client_private_key.pem', 'rb') as f:
        __client_private_key = f.read()
        __client_private_key = rsa.PrivateKey.load_pkcs1(__client_private_key)
    with open(dir+'serve_public_key.pem', 'rb') as f:
        __serve_public_key = f.read()
        __serve_public_key = rsa.PublicKey.load_pkcs1(__serve_public_key)
    with open(dir+'client_public_key.pem', 'rb') as f:
        __client_public_key = f.read()
        __client_public_key = rsa.PublicKey.load_pkcs1(__client_public_key)
    with open(dir+'serve_private_key.pem', 'rb') as f:
        __serve_private_key = f.read()
        __serve_private_key = rsa.PrivateKey.load_pkcs1(__serve_private_key)

    def __init__(self):
        pass

    def client_public_key(self):
        return self.__client_public_key

    def client_private_key(self):
        return self.__client_private_key

    def serve_private_key(self):
        return self.__serve_private_key

    def serve_public_key(self):
        return self.__serve_public_key

    

    