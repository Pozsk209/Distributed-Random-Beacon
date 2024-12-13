import binascii
import random
import hashlib
import math


def power_mod(x, m, n):
    ans = 1
    base = x % n
    if (m == 0):
        return 1 % n
    while (m):
        if (m & 1):
            ans = (ans * base) % n
        m = m >> 1
        base = (base * base) % n
    return ans


def primitive_root(p, q):  # 寻找原根
    if p == 2:
        return 1
    p1 = q
    p2 = (p - 1) // q

    while (1):
        g = random.randint(2, p - 1)

        if not (pow(g, (p - 1) // p1, p) == 1):
            if not pow(g, (p - 1) // p2, p) == 1:
                return g


'''
def is_prime(num):  # The Rabin-Miller Primality Test

    s = num - 1
    t = 0
    while s % 2 == 0:
        # 计算num -1 = 2^{t}*s
        s = s // 2
        t += 1
        for trials in range(5):  # 判断5次
            a = random.randrange(2, num - 1)
            v = pow(a, s, num)  # a^{s} mod num
            if v != 1:  # 判断a^{2^{r}*s} mod num是否为num-1
                i = 0
                while v != (num - 1):
                    if i == t - 1:
                        return False
                    else:
                        i = i + 1
                        v = (v ** 2) % num  # a^{2s},a^{4s},...,a^{2^{t}*s} mod num
            return True
'''


def MRwitness(n, x):
    b = 1
    m = n // 2
    while m % 2 == 0:
        b = b + 1
        m = m // 2
    j = 0
    z = power_mod(x, m, n)
    if z == 1:
        return 0
    while j < b and z != 1:
        y = z
        z = (z ** 2) % n
        j = j + 1
    return (z != 1) or (y != n - 1)


def is_prime(n):
    t = 10
    if n <= 1:
        return 0
    elif n == 2:
        return 1
    else:
        for i in range(t):
            x = random.randint(2, n - 1)
            if MRwitness(n, x):
                return 0
        return 1


def exgcd(a, b):  # 扩展欧几里得算法求孙子定理中Mi的逆元
    if b == 0:
        x = 1
        y = 0
        return a, x, y
    else:
        r, x, y = exgcd(b, a % b)
        y, x = x - (a // b) * y, y
    return r, x, y


def inv_mod(a, m):  # 求逆元函数，需要调用exgcd
    r, x, y = exgcd(a, m)
    if r != 1:
        return None
    else:
        return (x + m) % m  # 防止出现负数


def gen_prime(size):
    q = 4
    while not is_prime(q):
        q = random.randrange(2 ** (size - 1), 2 ** size)
    r = 2
    p = 4
    while not is_prime(p):
        r += 1
        p = r * q + 1
    return p, q, r

def decToOctet(x):
    temp = hex(x)[2:]
    if temp[-1] == 'L':
        temp = temp[:-1]
    if len(temp) & 1 == 1:
        temp = '0%s' % temp
    #print(binascii.unhexlify(temp))
    return binascii.unhexlify(temp)

def Hash(num):
    return int(binascii.hexlify(hashlib.sha512(num).digest()), 16)