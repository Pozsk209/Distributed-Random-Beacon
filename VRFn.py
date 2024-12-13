import hashlib
import random
import NumberTheory as NT


# |E|=p-1=2q
# |G|=q

class VRFn:
    # 选取的大素数p
    PRIME = int("\
    FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1\
29024E088A67CC74020BBEA63B139B22514A08798E3404DD\
EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245\
E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED\
EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D\
C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F\
83655D23DCA3AD961C62F356208552BB9ED529077096966D\
670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B\
E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9\
DE2BCBF6955817183995497CEA956AE515D2261898FA0510\
15728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)

    q = (PRIME - 1) // 2  # 群的阶

    g = 2  # 群的生成元

    f = 2  # 辅助因子

    def __init__(self):
        pass

    def Keygen(self, l=2048):
        x = random.randint(0, VRFn.q - 1) % VRFn.q  # 选取的私钥SK
        SK = x
        PK = NT.power_mod(VRFn.g, x, VRFn.PRIME)
        return SK, PK

    def Hashing(self, alpha, x):
        """

        :param alpha: 消息
        :param x: 私钥
        :return: VRFn证明(gamma,c,s) VRFn散列beta
        """

        '''VRFn的hash部分'''

        h = NT.Hash(alpha)  # 是不是没有映射到群上

        gamma = NT.power_mod(h, x, VRFn.PRIME)

        k = random.randint(0, VRFn.q - 1) % VRFn.q

        c = NT.Hash(
            NT.decToOctet(VRFn.g) + NT.decToOctet(h) + NT.decToOctet(NT.power_mod(VRFn.g, x, VRFn.PRIME)) + NT.decToOctet(
                NT.power_mod(h, x, VRFn.PRIME)) + NT.decToOctet(NT.power_mod(VRFn.g, k, VRFn.PRIME)) + NT.decToOctet(
                NT.power_mod(h, k, VRFn.PRIME))) % VRFn.q
        s = (VRFn.q + k - (c * x) % VRFn.q) % VRFn.q
        beta = NT.Hash(NT.decToOctet(NT.power_mod(gamma, VRFn.f, VRFn.PRIME)))
        pi = (gamma, c, s)  # 是这样吗

        return pi, beta
        # 输出生成的密钥和散列值beta

    def Verify(self, alpha, PK, *pi):
        '''验证过程'''
        h = NT.Hash(alpha)
        gamma = pi[0]
        c = pi[1]
        s = pi[2]
        u = (NT.power_mod(PK, c, VRFn.PRIME) * NT.power_mod(VRFn.g, s, VRFn.PRIME)) % VRFn.PRIME
        v = (NT.power_mod(gamma, c, VRFn.PRIME) * NT.power_mod(h, s, VRFn.PRIME)) % VRFn.PRIME  # 这个不一样
        """
        print("u:", u)
        print("g^k:", NT.power_mod(g, k, VRFn.PRIME))

        print("v:", v)
        print("h^k:", NT.power_mod(h, k, PRIME))
        """

        c2 = NT.Hash(
            NT.decToOctet(VRFn.g) + NT.decToOctet(h) + NT.decToOctet(PK) + NT.decToOctet(gamma) + NT.decToOctet(
                u) + NT.decToOctet(v)) % VRFn.q

        beta = NT.Hash(NT.decToOctet(NT.power_mod(gamma, VRFn.f, VRFn.PRIME)))
        print(c2)
        print("c Ver:", c == c2)
        print("beta:", beta)

        return beta

