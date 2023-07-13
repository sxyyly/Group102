import secrets
import hashlib

a = 0
b = 7
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (x, y)

#ECDSA
#gcd   
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b
#扩展欧几里得求模逆
def Euc(a, m):
    if gcd(a, m) != 1 and gcd(a, m) != -1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    if u1 > 0:
        return u1 % m
    else:
        return (u1 + m) % m

#椭圆曲线加法、乘法
def add(m, n):
    if (m == 0):
        return n
    if (n == 0):
        return m
    he = []
    if (m != n):
        if (gcd(m[0] - n[0], p) != 1 and gcd(m[0] - n[0], p) != -1):
            return 0
        else:
            k = ((m[1] - n[1]) * Euc(m[0] - n[0], p)) % p
    else:
        k = ((3 * (m[0] ** 2) + a) * Euc(2 * m[1], p)) % p
    x = (k ** 2 - m[0] - n[0]) % p
    y = (k * (m[0] - x) - m[1]) % p
    he.append(x)
    he.append(y)
    return he

def mul(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = add(t, l)
        n = n - 1
    return t
#二次剩余相关
def isQR(n,p):
    return pow(n, (p - 1) // 2, p)

def QR(n,p):
    assert isQR(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if isQR(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r
def keygen():
    sk = int(secrets.token_hex(32), 16)
    pk = mul(sk, G)
    return sk,pk

#私钥签名
def Signiture_sk(sk, m):
    e = hash(m)
    k = secrets.randbelow(p)
    R = mul(k, G)
    r = R[0] % p
    s = gcd(k, n) * (e + r * sk) % n

    return (r, s)


def Deduce_signiture(sign,m):
    r = sign[0]
    s = sign[1]
    x = r % p
    y = QR(((x**3)+7),p)
    e = hash(m)
    
    P1 = (x,y)
    P2 = (x,p-y)
    sk1 = mul(s%n,P1)
    tmp = mul(e%n,G)
    tmp_i = (tmp[0],p-tmp[1])
    tmp_1 = add(sk1,tmp_i)
    pk1 = mul(gcd(r,n),tmp_1)

    sk2 = mul(s%n,P2)
    tmp_2 = add(sk2,tmp_i)
    pk2 = mul(gcd(r,n),tmp_2)
    return pk1,pk2

    
if __name__ == '__main__':
    sk,pk = keygen()
    print("公钥: \n" ,pk)
    m = "20210046"
    p1,p2 = Deduce_signiture(Signiture_sk(sk, m),m)
    print('\n恢复公钥：')
    print(p1)
    print(p2)
