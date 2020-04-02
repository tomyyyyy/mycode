
import pyDHE
import sys

class sessionkey():
    """
        通过Ra, Rb产生会话密钥并保存到本地
    """

    __session_dir = "D:\\my code\\python密码学\\res\\sessionkey\\"

    def __init__(self):
        pass

    def client_sessionkey(self,Ra_save,Rb):
        global cli_sessionkey
        cli_sessionkey = Ra_save.update(Rb)
        with open(self.__session_dir+'client_session_key', "w") as x: 
            x.write(str(cli_sessionkey))

        return cli_sessionkey

    def get_client_sessionkey(self):
        return cli_sessionkey

    def serve_sessionkey(self,Rb,Rb_save):
        global ser_sessionkey
        ser_sessionkey = Rb_save.update(Rb)
        with open(self.__session_dir+'serve_session_key', "w") as x:  
            x.write(str(ser_sessionkey))
            
        return ser_sessionkey

    def get_serve_sessionkey(self):
        return ser_sessionkey
