from Math import randint

import SM2
import Util
from SM2KeyPair import SM2KeyPair
import SM3
from User import User

import time

def generator_key_pair():
    d = randint(1, SM2.sm2.n - 2)
    P = SM2.sm2.get_g() * d
    return SM2KeyPair(d, P)


def encrypt(user: User, message: bytearray, op):
    PB = user.sm2_key_pair.public_key.P#公钥
    curve = PB.curve
    while True:
        # A1
        k = randint(1, curve.n - 1)
        # A2
        C1 = curve.get_g() * k
        C1 = Util.ECPoint_2_bytes(C1, op)

        # A3
        S = PB * curve.h
        if S.is_identity():#确保S不是无穷远点
            raise ValueError("S是单位元")
        # A4
        kPB = PB * k
        x2, y2 = kPB.get_x(), kPB.get_y()
        x2 = Util.int_2_bytes(x2, curve.l)
        y2 = Util.int_2_bytes(y2, curve.l)
        # A5
        t = Util.KDF(Util.join(x2, y2), len(message) << 3)
        if not Util.is_all_zero(t):
            break
    # A6
    C2 = Util.xor_two_array(message, t)
    # A7
    C3 = SM3.hash(Util.join(x2, message, y2))
    return Util.join(C1, C3, C2)

if __name__ == "__main__":
    ID = "2023".encode()
    db = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
    xb = 0x435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A
    yb = 0x75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42
    d = db#私钥
    P = SM2.sm2.create_point(xb, yb)
    msg = "hello world".encode()
    u = User(ID, SM2KeyPair(d, P))
    start=time.time()
    c = encrypt(u, msg, 0)
    end=time.time()
    print(end-start)
    print("用户ID为:",ID)
    print("私钥：",d)
    print("公钥",P)
    print("消息：",msg)
    print("密文",c)