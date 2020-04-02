
import rsa
import base64
import hashlib
from lib.key import key

class rsacrypto():
    __encrypto_length = 117
    __decrypto_length = 128

    def __init__(self):
        pass

    def rsa_encrypt(self, message, pkey):
        '''
            加密长度位117byte
            message:        String 加密的内容
            text_encrypt:   bytes 加密后的内容
        '''
        encrypt_text = []
        for i in range(0, len(message), self.__encrypto_length):
            cont = message[i:i+self.__encrypto_length]
            encrypt_text.append(rsa.encrypt(cont.encode(), pkey))

        # 加密完进行拼接
        cipher_text = b''.join(encrypt_text)
        text_encrypt = cipher_text
        # base64进行编码
        # text_encrypt = base64.b64encode(cipher_text)
        # text_encrypt = text_encrypt.decode()

        return text_encrypt

    def client_encrypt(self, message):
        global client_public_key                    
        client_public_key = key().client_public_key()
        text_encrypt = self.rsa_encrypt(message,client_public_key)

        return text_encrypt

    def serve_encrypt(self, message):
        global serve_public_key                    
        serve_public_key = key().serve_public_key()
        text_encrypt = self.rsa_encrypt(message, serve_public_key)

        return text_encrypt

    def rsa_decrypt(self, text_encrypt, pkey):
        """
            私钥进行解密
            加密后密文的长度为密钥的长度，如密钥长度为 1024b(128Byte)，最后生成的密文固定为 1024b(128Byte)
            text_encrypt: bytes
            return:  String
        """
        # text_encrypt = text_encrypt.encode()
        # base64解码
        # msg = base64.b64decode(text_encrypt)
        # msg = bytes()

        msg = text_encrypt
        # 进行解密
        text = []
        for i in range(0, len(msg), self.__decrypto_length):
            cont = msg[i:i+self.__decrypto_length]
            text.append(rsa.decrypt(cont, pkey))
        text = b''.join(text)
        return text.decode()

    def client_decrypt(self, text_encrypt):
        global client_private_key
        client_private_key = key().client_private_key()
        text = self.rsa_decrypt(text_encrypt, client_private_key)

        return text

    def serve_decrypt(self, text_encrypt):
        global serve_private_key
        serve_private_key = key().serve_private_key()
        text = self.rsa_decrypt(text_encrypt, serve_private_key)

        return text

    def rsa_sign(self, message, pkey):
        """
            message: String
            key: bytes
            return:  bytes
        """
        summary = hashlib.md5(str(message).encode()).hexdigest()
        message = str(summary).encode("utf-8")
        message_sign = rsa.sign(message,pkey,"SHA-256")

        return message_sign

    def client_sign(self,message):
        global client_private_key
        client_private_key = key().client_private_key()
        message_sign = self.rsa_sign(message, client_private_key)

        return message_sign

    def serve_sign(self,message):
        global serve_private_key
        serve_private_key = key().serve_private_key()
        message_sign = self.rsa_sign(message, serve_private_key)

        return message_sign

    def rsa_verify(self, content, sign, pkey):
        """
            content: String
            sign: bytes
            key: bytes
        """
        summary = hashlib.md5(str(content).encode()).hexdigest()
        summary = str(summary).encode()
        verify = rsa.verify(summary, sign, pkey)

        return verify