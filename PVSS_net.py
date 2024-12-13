import random
import Schnorr_Group as SG
import NumberTheory as NT
import hashlib


class PVSS:
    """

    """

    def __init__(self, n, t, uid, secure_number):
        """
        初始化
        :param n:
        :param t:
        :param uid:
        :param secure_number:
        """

        self.Gq = SG.SchnorrGroup(secure_number)
        self.p = self.Gq.p
        self.q = self.Gq.q
        self.G = self.Gq.G
        self.g = self.Gq.g

        self.n = n
        self.t = t
        self.uid = uid

        self.a_q = [0] * t  # 模q的系数
        self.a_p = [0] * t  # Zp中的系数
        self.alpha = [0] * t

        self.pri_key = [0] * n
        self.pri_inv = [0] * n  # 私钥的逆
        self.pub_key = [0] * n

        self.member_commitments = []
        self.other_commitments = [[]] * n
        self.other_pub_key = [0] * n
        self.my_HX = [0] * n  # 给别人计算发出去的，序号是按照uid排的
        self.my_HY = [0] * n
        self.Hw = [0] * n
        self.a1 = [0] * n
        self.a2 = [0] * n
        self.p_uid = [0] * n
        self.other_p = [0] * n
        self.other_q = [0] * n
        self.other_g = [0] * n
        self.other_HY = [0] * n  # 别人利用我的公钥返回给我的加密碎片，一共n-1个人给我，我自己尚未给我
        self.s = 0  # 秘密
        self.challenge = 0
        self.dec_challenge = [0] * n
        self.other_ri = [0] * n

    def change_field(self, p=None, q=None, G=None, g=None):
        self.Gq.change(p, q, g, G)
        self.p = p
        self.q = q
        self.G = G
        self.g = g

    def key_gen(self, other_uid, other_p, other_q, other_g):
        """
        生成公钥，用于给别人，让别人加密，因此需要别人的p和q
        :param other_p:
        :param other_q:
        :return:
        """
        other_uid -= 1
        while self.pri_key[other_uid] == 0:
            self.pri_key[other_uid] = self.Gq.getnumber(random.randrange(1, other_q)) % other_q
        self.pri_inv[other_uid] = NT.inv_mod(self.pri_key[other_uid], other_q)
        self.pub_key[other_uid] = NT.power_mod(other_g, self.pri_key[other_uid], other_p)
        self.other_pub_key[self.uid - 1] = self.pub_key[other_uid]

    def secret_chosen(self):
        """
        生成秘密，是自己的，故p和q是自己的
        :return:
        """
        self.s = self.Gq.getnumber(random.randrange(0, self.q))
        print("s_ch:", self.s)
        self.a_p[0] = self.s
        self.a_q[0] = self.s % self.q
        self.s = NT.power_mod(self.g, self.s % self.q, self.p)

    def gen_coefficients(self):
        for i in range(1, self.t):
            self.a_p[i] = self.Gq.getnumber(random.randrange(0, self.q))
            self.a_q[i] = self.a_p[i] % self.q

    def f(self, x):
        y = 0
        for i in range(self.t):
            y = (self.a_q[i] * pow(x, i, self.q) + y) % self.q
        return y

    def commitment(self):
        for i in range(self.t):
            self.member_commitments.append(pow(self.g, self.a_q[i], self.p))

    def generate(self):
        # PVSS.key_gen(self)
        PVSS.secret_chosen(self)
        PVSS.gen_coefficients(self)
        PVSS.commitment(self)

    def distribute_secret(self, uid, other_p):
        """
        分发自己的秘密给别人，但是别人给我的公钥，我要用他的p，别人没给我的，我用自己的
        :param uid:
        :return:
        """
        self.p_uid[uid - 1] = PVSS.f(self, uid) % self.q
        HY = NT.power_mod(self.other_pub_key[uid - 1], self.p_uid[uid - 1], other_p)
        HX = NT.power_mod(self.g, self.p_uid[uid - 1], other_p)
        self.my_HX[uid - 1] = HX  # 别人的公钥加密我的秘密
        self.my_HY[uid - 1] = HY
        return HY  # 我不知道应该返回什么

    def a1a2(self):
        self.Hw[self.uid - 1] = self.Gq.getnumber(random.randrange(0, self.q))
        self.a1[self.uid - 1] = NT.power_mod(self.g, self.Hw[self.uid - 1], self.p)
        self.a2[self.uid - 1] = NT.power_mod(self.pub_key[self.uid - 1], self.Hw[self.uid - 1], self.p)

    def share_correctness(self, uid):
        Hashtmp = hashlib.sha256()
        strHash = ""
        strHX = ""
        strHY = ""
        stra1 = ""
        stra2 = ""
        for i in range(self.n):
            strHX += str(self.my_HX[i])
            strHY += str(self.my_HY[i])
            stra1 += str(self.a1[i])
            stra2 += str(self.a2[i])
        strHash = strHX + strHY + stra1 + stra2
        Hashtmp.update(strHash.encode("UTF-8"))
        if self.challenge == 0:
            self.challenge = int(Hashtmp.hexdigest(), 16) % self.q
        r_uid = (self.Hw[uid - 1] - self.p_uid[uid - 1] * self.challenge) % self.q
        return self.challenge, r_uid

    def share_verification(self, other_uid, ri):
        """
        验证别人的正确性
        :return:
        """
        other_uid -= 1
        rightc = 1
        for i in range(self.t):
            rightc = rightc * NT.power_mod(self.other_commitments[other_uid][i],
                                           NT.power_mod(self.uid, i, self.other_q[other_uid]),
                                           self.other_p[other_uid]) % self.other_p[other_uid]
        print("right", rightc)
        print(ri)
        print("cc", self.other_HY[other_uid])
        a1i = NT.power_mod(self.g, ri, self.p) * NT.power_mod(rightc, self.challenge, self.p) % self.p
        a2i = NT.power_mod(self.pub_key[other_uid], ri, self.p) * NT.power_mod(self.other_HY[other_uid], self.challenge, self.p) % self.p
        print(a1i)
        print(a2i)
        print(NT.power_mod(self.g, self.Hw[self.uid - 1], self.p))
        print(NT.power_mod(self.pub_key[other_uid], self.Hw[self.uid - 1], self.p))

        return rightc, a1i, a2i



    def share_decrypt(self, uid, other_p):
        uid -= 1
        print(self.other_HY)
        print(self.pri_inv)
        print(self.pri_key)
        print(self.pub_key)
        return NT.power_mod(self.other_HY[uid], self.pri_inv[uid], other_p)

    def share_decryption_correctness_proof(self, other_uid, S):
        other_uid -= 1
        a1i = NT.power_mod(self.g, self.Hw[other_uid], self.p)
        a2i = NT.power_mod(S, self.Hw[other_uid], self.p)
        hashtmp = hashlib.sha256()
        strhash = str(self.other_pub_key[other_uid]) + str(self.other_HY[other_uid]) + str(a1i) + str(a2i)
        hashtmp.update(strhash.encode("UTF-8"))
        self.dec_challenge[other_uid] = int(hashtmp.hexdigest(), 16) % self.q
        return self. dec_challenge[other_uid]

    def share_decryption_verification(self, other_uid, ri, S):
        a1i = NT.power_mod(self.g, ri, self.p) * NT.power_mod(self.pub_key[other_uid], self.challenge, self.p) % self.p
        a2i = NT.power_mod(S, ri, self.p) * NT.power_mod(self.other_HY[other_uid], self.challenge, self.p) % self.p
        hashtmp = hashlib.sha256()
        strhash = str(self.pub_key[other_uid]) + str(self.other_HY[other_uid]) + str(a1i) + str(a2i)
        hashtmp.update(strhash.encode("UTF-8"))
        dec_c = int(hashtmp.hexdigest(), 16) % self.q
        return dec_c

    def reconstruct(self, p, q, partyuid=None, partysec=None):
        """

        :param q:
        :param people:
        :param party:
        :return:
        """
        num = len(partyuid)
        s_re = 1
        if num < self.t:
            print("参与者人数需多于门限值")
        elif num > self.n:
            print("人数过多")
        else:
            for i in range(num):
                d = 1
                for j in range(num):
                    if partyuid[i] == partyuid[j]:
                        continue
                    else:
                        #print("i,j", partyuid[i], partyuid[j])
                        d = (-partyuid[j] * NT.inv_mod(partyuid[i] - partyuid[j], q) % q) * d % q
                s_re = (s_re * NT.power_mod(partysec[i], d, p)) % p
        return s_re

    def prints(self):
        print("s:", self.s)
        print("s%q", self.a_q[0])

    def getvalue(self, other_uid, p, q, g, w, pubkey, other_com=None):
        self.setvalue = True
        other_uid -= 1
        # self.member_shares[other_uid] = other_si
        self.other_pub_key[other_uid] = pubkey
        self.other_p[other_uid] = p
        self.other_q[other_uid] = q
        self.other_g[other_uid] = g
        self.Hw[other_uid] = w
        self.a1[other_uid] = NT.power_mod(self.g, w, self.p)
        self.a2[other_uid] = NT.power_mod(pubkey, w, self.p)
        for i in range(self.t):
            self.other_commitments[other_uid].append(other_com[i])

    def send_pubkey(self, uid):
        return self.pub_key[uid - 1]

    def sendvalue(self, uid):
        return str(self.uid) + ":" + str(self.p) + ":" + str(self.q) + ":" + str(self.g) + ":" + str(
            self.pub_key[uid - 1]) + ":" + str(self.member_commitments)


p1 = PVSS(4, 3, 1, 8)  # 一个程序
p2 = PVSS(4, 3, 2, 8)  # 两个程序
p3 = PVSS(4, 3, 3, 8)  # 三个程序
p4 = PVSS(4, 3, 4, 8)  # 四个程序

#p1.change_field(p2.p, p2.q, p2.G, p2.g)
#p3.change_field(p2.p, p2.q, p2.G, p2.g)
#p4.change_field(p2.p, p2.q, p2.G, p2.g)

print(p1.p, p1.q, p1.g)
print(p2.p, p2.q, p2.g)
print(p3.p, p3.q, p3.g)
print(p4.p, p4.q, p4.g)

p1.generate()
p2.generate()
p3.generate()
p4.generate()

p1.key_gen(2, p2.p, p2.q, p2.g)
p2.key_gen(2, p2.p, p2.q, p2.g)
p3.key_gen(2, p2.p, p2.q, p2.g)
p4.key_gen(2, p2.p, p2.q, p2.g)

p1.a1a2()
p2.a1a2()
p3.a1a2()
p4.a1a2()

print(p1.send_pubkey(2))
print(p3.send_pubkey(2))
print(p4.send_pubkey(2))

p2.getvalue(1, p1.p, p1.q, p1.g, p1.Hw[0], p1.send_pubkey(2), eval(p1.sendvalue(2).split(":")[-1]))
p2.getvalue(3, p3.p, p3.q, p3.g, p1.Hw[2], p3.send_pubkey(2), eval(p3.sendvalue(2).split(":")[-1]))
p2.getvalue(4, p4.p, p4.q, p4.g, p1.Hw[3], p4.send_pubkey(2), eval(p4.sendvalue(2).split(":")[-1]))



p1.getvalue(2, p2.p, p2.q, p2.g, p2.Hw[1], p2.send_pubkey(1), eval(p2.sendvalue(1).split(":")[-1]))

p1.other_HY[2 - 1] = p2.distribute_secret(1, p2.p)
p3.other_HY[2 - 1] = p2.distribute_secret(3, p2.p)
p4.other_HY[2 - 1] = p2.distribute_secret(4, p2.p)

p2.distribute_secret(2, p2.p)



print("p2 com:", p2.member_commitments)
p2.prints()

p1.challenge, p1.other_ri[1] = p2.share_correctness(1)
p2.share_correctness(3)
p2.share_correctness(4)


print("c", p1.my_HX)

p1.share_correctness(2)
p1.share_verification(2, p1.other_ri[1])

p3.share_correctness(2)
p3.share_verification(2, p3.other_ri[1])

p3.share_correctness(2)
p3.share_verification(2, p3.other_ri[1])



pty = [p1.share_decrypt(2, p2.p), p3.share_decrypt(2, p2.p), p4.share_decrypt(2, p2.p)]
pty2 = [NT.power_mod(p2.g, p2.p_uid[0], p2.p), NT.power_mod(p2.g, p2.p_uid[2], p2.p),
        NT.power_mod(p2.g, p2.p_uid[3], p2.p)]  # 正确的
print("pty", pty)
print("pty2", pty2)

print(p2.reconstruct(p2.p, p2.q, [1, 3, 4], pty))
print(p2.reconstruct(p2.p, p2.q, [1, 3, 4], pty2))
