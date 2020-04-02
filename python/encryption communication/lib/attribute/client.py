
import random
import pyDHE
import time
import hashlib
from res.key import key


class client():
    """
        client的各种属性
    """
    __MAX = 12322145625621452524554561

    A = key().serve_public_key()
    B = key().client_public_key()
    ra = 0
    rb = 0
    Ra = 0
    Ra_md5 = hashlib.md5(str(Ra).encode()).hexdigest()
    Rb = 0
    Rb_md5 = hashlib.md5(str(Rb).encode()).hexdigest()
    T = 0
    sessionkey = 0


    def __init__(self,A,B,ra,rb,Ra,Rb,T,seesionkey):
        self.A = A
        self.B = B
        self.ra = ra
        self.rb = rb
        self.Ra = Ra
        self.Rb = Rb
        self.T = T
        self.sessionkey = seesionkey

    def produce_ra(self):
        global ra
        ra = random.randint(0,self.__MAX)
        return ra

    def produce_Ra(self):
        global Ra
        Ra = pyDHE.new()
        return Ra

    def produce_T(self):
        global T
        T = int(time.time())
        return T
