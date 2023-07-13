import ECMH_project
import random
from Crypto.Cipher import AES
from gmssl import sm2
import time

def SM2_enc(plaintext):
    ciphertext = sm2_crypt.encrypt(plaintext)
    return ciphertext


# SM2 decryption
def SM2_dec(ciphertext):
    plaintext = sm2_crypt.decrypt(ciphertext)
    return plaintext


def PGP_Encrypt(mes, k):
    mode = AES.MODE_OFB
    iv = b'0000000000000000'
    cryptor = AES.new(k.encode('utf-8'), mode, iv)
    length = 16
    count = len(mes)
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    mes = mes + ('\0' * add)
    ciphertext1 = cryptor.encrypt(mes.encode('utf-8'))
    plaintext_bytes = k.encode('utf-8')
    ciphertext2 = SM2_enc(plaintext_bytes)
    print("用会话密钥加密的消息值：", ciphertext1)
    print("用SM2公钥得到会话密钥的加密结果：", ciphertext2)
    return ciphertext1, ciphertext2


def PGP_Decrypt(mes1, mes2):
    mode = AES.MODE_OFB
    iv = b'0000000000000000'
    get_key = SM2_dec(mes2)
    print("用SM2私钥得到会话密钥：", get_key.decode('utf-8'))
    cryptor = AES.new(get_key, mode, iv)
    plain_text = cryptor.decrypt(mes1)
    print("原消息值", plain_text.decode('utf-8'))


if __name__ == '__main__':
    start=time.time()
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    G = [Gx, Gy]
    [sk, pk] = ECMH_project.key_gen(a, p, n, G)
    sk_bytes = hex(sk)[2:]
    pk_bytes = hex(pk[0])[2:] + hex(pk[1])[2:]

    sm2_crypt = sm2.CryptSM2(public_key=pk_bytes, private_key=sk_bytes)
    msg = "Hello World!"
    print("受保护的消息：", msg)
    k = hex(random.randint(2 ** 127, 2 ** 128))[2:]
    print("随机生成的对称加密密钥(会话密钥)：", k)
    result1, result2 = PGP_Encrypt(msg, k)
    end=time.time()
    print("加密时间：",end-start)
    start=time.time()
    PGP_Decrypt(result1, result2)
    end=time.time()
    print("解密时间：",end-start)