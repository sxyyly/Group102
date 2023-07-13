#伪装中本聪
import random
import time
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
def ECDSA_sig(m, n, G, d,k):
    e = hash(m)
    R = mul(k, G)
    r = R[0] % n
    s = (Euc(k, n) * (e + d * r)) % n
    return r, s

def forge_verify(e, n, G, r, s, P):
    w = Euc(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = add(mul(v1, G), mul(v2, P))
    if (w == 0):
        return 
    else:
        if (w[0] % n == r):
            print("验证成功！")
            print("forge signiture:",r1,s1)
            return 1


m="2022"
m_1="xxxx"
x=5
y=1
G = [5, 1]
a = 2
b = 2
p = 17
n = 19
k=2
d = 5
P = mul(d, G)

r,s=ECDSA_sig(m,n,G,d,k)
print("forge_BItcoin project:伪装中本聪")
print("signiture:",r,s)
start=time.time()
a= random.randrange(1, n - 1)
b = random.randrange(1, n - 1)
r1 = add(mul(a, G), mul(b, P))[0]
e1 = (r1 * a * Euc(b, n)) % n
s1 = (r1 * Euc(b, n)) % n
forge_verify(e1, n, G, r1, s1, P)
end=time.time()
print(end-start)

