"""
我们初步的思想是每生成一个实例，就为其返回一个唯一的标号
第一个人必须输入总人数n和门限值t。在这个阶段，所有标号会提前约定好，当新生成一个实例时，标号就会分发
然后每个参与者分发的秘密，就根据标号，秘密地分发给其他参与者。可以根据标号（或者实例的id）来确定其是否有资格知晓这个秘密。

后期可以设置重置函数

"""

import random
import Zp_Group
import hashlib


class PVSSn:
    n = None
    t = None
    G = Zp_Group.Zp_Group()
    p = G.p
    q = G.q
    g = G.g
    a = G.a
    r = G.r
    a_enc = G.a_enc
    Zp = G.Zp_star
    member_secrets = []
    member_commitments = []
    pi = []

    pri_key = []
    pri_inv = []

    pub_key = []

    HX = []  # 5x5
    HY = []  # 5x5
    Hw = []  # 5x5
    a1 = []  # 5x5
    a2 = []  # 5x5
    ri = []  # 5x5
    # chg = hashlib.sha256() #challenge本来是用hash来生成的，这里先用随机数
    chg = []  # 五个hash

    def __init__(self, n, t):
        """
        构造函数，初始化变量
        :param n: 参与者人数
        :param t: 门限值
        """
        if PVSSn.n is None:
            PVSSn.n = n
            PVSSn.key_gen(self)

        if PVSSn.t is None:
            PVSSn.t = t

        self.a_q = [None] * t  # 模q的系数
        self.a_p = [None] * t  # Zp中的系数
        self.alpha = [None] * t
        # self.NIZK_proof = []

        if len(PVSSn.member_secrets) == 0:
            PVSSn.member_commitments = [[None] * t for i in range(n)]
            PVSSn.member_secrets = [[None] * n for i in range(n)]
            PVSSn.pi = [[None] * n for i in range(n)]
            PVSSn.ri = [[None] * n for i in range(n)]
            PVSSn.HX = [[None] * n for i in range(n)]
            PVSSn.HY = [[None] * n for i in range(n)]
            PVSSn.Hw = [[None] * n for i in range(n)]
            PVSSn.a1 = [[None] * n for i in range(n)]
            PVSSn.a2 = [[None] * n for i in range(n)]
            PVSSn.chg = [None] * n

            for i in range(PVSSn.n):
                for j in range(PVSSn.n):
                    PVSSn.Hw[i][j] = Zp_Group.Number_in_Zp(int(random.choice(PVSSn.G)), PVSSn.q)
                    PVSSn.a1[i][j] = Zp_Group.Number_in_Zp(PVSSn.a ** int(PVSSn.Hw[i][j]), PVSSn.p)
                    PVSSn.a2[i][j] = Zp_Group.Number_in_Zp(int(PVSSn.pub_key[j]) ** int(PVSSn.Hw[i][j]), PVSSn.p)

    def key_gen(self):
        """
        生成参与者的公钥和私钥以及私钥的逆
        :return:无
        """
        tmp = Zp_Group.Number_in_Zp(PVSSn.a_enc, PVSSn.p)
        for i in range(PVSSn.n):
            x = random.choice(PVSSn.G)
            PVSSn.pri_key.append(x)
            x_inv = Zp_Group.Number_in_Zp(1, PVSSn.q) // Zp_Group.Number_in_Zp(int(x), PVSSn.q)
            PVSSn.pri_inv.append(x_inv)
            PVSSn.pub_key.append(tmp ** x)
        return

    def secret_chosen(self):
        """
        秘密选择函数，在子群G上随机选择并用公钥加密
        :return: 无
        """
        s = random.choice(PVSSn.G)  # 选择的s需要小于q
        # print("s:", s)
        self.a_p[0] = s
        self.a_q[0] = s.change_modulo(PVSSn.q)
        self.s = Zp_Group.Number_in_Zp(PVSSn.a_enc ** (int(s) % PVSSn.q), PVSSn.p)

        # print("s:", self.s)
        # return self.s
        return

    def get_secret(self):
        """
        直接获取实例的随机数S
        :return:随机数S
        """
        return [int(self.s), int(self.a_q[0])]

    def gen_coefficients(self):
        """
        生成多项式系数
        :return: 无
        """
        for i in range(1, PVSSn.t):
            self.a_p[i] = random.choice(PVSSn.G)
            self.a_q[i] = self.a_p[i].change_modulo(PVSSn.q)
            # print("a_q:", self.a_q[i])
        return

    def f(self, x):
        """
        f函数计算秘密碎片f(x)
        :param x:x，用于计算f(x)，常使用参与者下标
        :return:f(x)
        """
        tmpx = Zp_Group.Number_in_Zp(x, PVSSn.q)
        y = Zp_Group.Number_in_Zp(0, PVSSn.q)
        for i in range(PVSSn.t):
            y += self.a_q[i] * (tmpx ** i)
        return y

    def Commitment(self, index):
        """
        生成系数的承诺，用于检验碎片的正确性
        :param index:参与方在f函数输入的值，常使用下标，务必与f函数输入参数一致
        :return:无
        """
        tmpa = Zp_Group.Number_in_Zp(PVSSn.a, PVSSn.p)
        for i in range(PVSSn.t):
            self.alpha[i] = tmpa ** self.a_p[i]
            PVSSn.member_commitments[index - 1][i] = self.alpha[i]
        return

    def Generate(self, index):  # index是成员的分配的下标 1,2,3,... ,n
        """
        生成或者重新生成，包括随机选择的秘密，多项式系数以及相关的承诺。
        :param index:参与者输入值，通常是下标
        :return:无
        """
        self.shares = []

        # PVSSn.key_gen(self)
        PVSSn.secret_chosen(self)
        PVSSn.gen_coefficients(self)  # 说明每个人的多项式不一样
        ag = Zp_Group.Number_in_Zp(PVSSn.a, PVSSn.p)
        for i in range(1, PVSSn.n + 1):
            PVSSn.pi[index - 1][i - 1] = PVSSn.f(self, i)
            pubkey = Zp_Group.Number_in_Zp(int(PVSSn.pub_key[i - 1]), PVSSn.p)
            # print("pi:", PVSSn.pi[index - 1][i - 1])
            # print(PVSSn.a_enc ** int(PVSSn.pi[index - 1][i - 1]) % PVSSn.p)
            PVSSn.HX[index - 1][i - 1] = ag.__pow__(int(PVSSn.pi[index - 1][i - 1]), PVSSn.p)  # 计算X
            PVSSn.HY[index - 1][i - 1] = pubkey.__pow__(int(PVSSn.pi[index - 1][i - 1]), PVSSn.p)  # 计算Y 实际就是要公开的秘密
            # PVSSn.ri[index - 1][i] = PVSSn.Hw[index - 1][i] - pi*

            # PVSSn.member_secrets[index - 1].append(PVSSn.HY[index - 1][i - 1])  # 压入公共列表
            # print("shares:", self.shares[i - 1])
        PVSSn.Commitment(self, index)  # 计算验证参数

        # ----------Hash----------------
        Hashtmp = hashlib.sha256()
        strHash = ""
        strHX = ""
        strHY = ""
        stra1 = ""
        stra2 = ""
        for i in range(PVSSn.n):
            strHX += str(PVSSn.HX[index - 1][i])
            strHY += str(PVSSn.HY[index - 1][i])
            stra1 += str(PVSSn.a1[index - 1][i])
            stra2 += str(PVSSn.a2[index - 1][i])
        strHash = strHX + strHY + stra1 + stra2
        # print("strhash", strHash)
        Hashtmp.update(strHash.encode("UTF-8"))
        PVSSn.chg[index - 1] = Zp_Group.Number_in_Zp(int(Hashtmp.hexdigest(), 16), PVSSn.p)  # challenge

        for i in range(PVSSn.n):
            pichg = Zp_Group.Number_in_Zp(int(PVSSn.pi[index - 1][i]) * int(PVSSn.chg[index - 1]), PVSSn.q)
            PVSSn.ri[index - 1][i] = PVSSn.Hw[index - 1][i] - pichg

        self.NIZK_proof = ([int(i) for i in PVSSn.member_commitments[index - 1]], int(PVSSn.chg[index - 1]),
                           [int(i) for i in PVSSn.ri[index - 1]])
        # return self.alpha
        return

    def Share_Verify(self, leader_idx):
        """
        验证自己self获得的来自分发者leader的碎片s的正确性。
        :param leader_idx: 密钥碎片发出者的下标
        :param self_idx: 自己的下标
        :return:bool型，s是否正确
        """
        tmp_hash = hashlib.sha256()

        '''
        tmpa = Zp_Group.Number_in_Zp(1, PVSSn.p)
        tmpg = PVSSn.HX[leader_idx - 1][self_idx - 1]
        for i in range(PVSSn.t):
            # tmpa = tmpa * (self.alpha[i] ** (j ** i))
            tmpa = tmpa * (PVSSn.member_commitments[leader_idx - 1][i] ** (self_idx ** i))
        print(tmpg)
        print(tmpa) #要把tmpa放入hash中对比
        '''
        for j in range(1, PVSSn.n + 1):
            tmpa = Zp_Group.Number_in_Zp(1, PVSSn.p)
            for i in range(PVSSn.t):
                # tmpa = tmpa * (self.alpha[i] ** (j ** i))
                tmpa = tmpa * (PVSSn.member_commitments[leader_idx - 1][i] ** (j ** i))
            tmp_hash.update(str(tmpa).encode("UTF-8"))

        for j in range(PVSSn.n):
            tmp_hash.update(str(PVSSn.HY[leader_idx - 1][j]).encode("UTF-8"))

        for j in range(1, PVSSn.n + 1):
            gr = Zp_Group.Number_in_Zp(int(PVSSn.a) ** int(PVSSn.ri[leader_idx - 1][j - 1]), PVSSn.p)
            # print("gr", gr)
            xc = Zp_Group.Number_in_Zp(int(PVSSn.HX[leader_idx - 1][j - 1]) ** int(PVSSn.chg[leader_idx - 1]), PVSSn.p)
            # print("xc", xc)
            tmpa1 = gr * xc
            tmp_hash.update(str(tmpa1).encode("UTF-8"))
            # print('tmpa1', tmpa1)

        """
        yr = Zp_Group.Number_in_Zp(int(PVSSn.pub_key[leader_idx - 1]) ** int(PVSSn.ri[leader_idx - 1][self_idx - 1]),
                                   PVSSn.p)
        # print("yr", yr)
        yc = Zp_Group.Number_in_Zp(int(PVSSn.HY[leader_idx - 1][self_idx - 1]) ** int(PVSSn.chg[leader_idx - 1]), PVSSn.p)
        # print("yc", yc)
        tmpa2 = yr * yc
        tmp_hash.update(str(tmpa2).encode("UTF-8"))
        print('tmpa2', tmpa2)"""

        for j in range(1, PVSSn.n + 1):
            yr = Zp_Group.Number_in_Zp(int(PVSSn.pub_key[j - 1]) ** int(PVSSn.ri[leader_idx - 1][j - 1]),
                                       PVSSn.p)
            # print("yr", yr)
            yc = Zp_Group.Number_in_Zp(int(PVSSn.HY[leader_idx - 1][j - 1]) ** int(PVSSn.chg[leader_idx - 1]), PVSSn.p)
            # print("yc", yc)
            tmpa2 = yr * yc
            tmp_hash.update(str(tmpa2).encode("UTF-8"))
            # print('tmpa2', tmpa2)

        num_tmp_hash = Zp_Group.Number_in_Zp(int(tmp_hash.hexdigest(), 16), PVSSn.p)

        # print('numhash', num_tmp_hash)

        if num_tmp_hash == PVSSn.chg[leader_idx - 1]:
            return True
        else:
            return False

    def share_decrypt(self):
        """
        碎片解密，用于恢复随机数
        :return:无
        """
        for i in range(PVSSn.n):
            for j in range(PVSSn.n):
                PVSSn.member_secrets[i][j] = Zp_Group.Number_in_Zp(int(PVSSn.HY[i][j]) ** int(PVSSn.pri_inv[j]), PVSSn.p)
                # 注意一下priinv是i还是j

        return

    def share_dec_verify(self, leader_idx, self_idx):
        """
        :param leader_idx: 秘密对应的leader
        :param self_idx: 验证者，理论上验证一个即可
        :return:验证成功或者失败
        """
        PVSSn.share_decrypt(self)
        tmpr = Zp_Group.Number_in_Zp(
            int(PVSSn.Hw[leader_idx - 1][self_idx - 1]) - int(PVSSn.pri_key[self_idx - 1]) * int(PVSSn.chg[self_idx - 1]),
            PVSSn.q)
        dv_Hash = hashlib.sha256()
        tmp_Hash = hashlib.sha256()
        H_str = str(PVSSn.pub_key[self_idx - 1]) + str(PVSSn.HY[leader_idx - 1][self_idx - 1]) + str(
            Zp_Group.Number_in_Zp(int(PVSSn.a_enc) ** int(PVSSn.Hw[leader_idx - 1][self_idx - 1]), PVSSn.p)) + str(
            Zp_Group.Number_in_Zp(
                int(PVSSn.member_secrets[leader_idx - 1][self_idx - 1]) ** int(PVSSn.Hw[leader_idx - 1][self_idx - 1]),
                PVSSn.p))
        dv_Hash.update(H_str.encode("UTF-8"))
        # print(dv_Hash.hexdigest())
        Gr = Zp_Group.Number_in_Zp(int(PVSSn.a_enc) ** int(tmpr), PVSSn.p)
        yc = Zp_Group.Number_in_Zp(int(PVSSn.pub_key[self_idx - 1]) ** int(PVSSn.chg[self_idx - 1]), PVSSn.p)
        tmpa1 = Gr * yc

        Sr = Zp_Group.Number_in_Zp(int(PVSSn.member_secrets[leader_idx - 1][self_idx - 1]) ** int(tmpr), PVSSn.p)
        Yc = Zp_Group.Number_in_Zp(int(PVSSn.HY[leader_idx - 1][self_idx - 1]) ** int(PVSSn.chg[self_idx - 1]), PVSSn.p)
        tmpa2 = Sr * Yc
        H_tmp = str(PVSSn.pub_key[self_idx - 1]) + str(PVSSn.HY[leader_idx - 1][self_idx - 1]) + str(tmpa1) + str(tmpa2)
        tmp_Hash.update(H_tmp.encode("UTF-8"))
        # print("H_str", H_str)
        # print("H_tmp", H_tmp)

        if tmp_Hash.hexdigest() == dv_Hash.hexdigest():
            return True
        else:
            return False

    def Reconstruct(self, people, party=None):
        """
        :param people: 被恢复的人
        :param party: 一个列表，表示要执行秘密重建的人的标号
        :return:  秘密值
        """
        PVSSn.share_decrypt(self)
        num = len(party)
        s_re = Zp_Group.Number_in_Zp(1, PVSSn.p)
        if num < PVSSn.t:
            print("参与者人数需多于门限值")
        elif num > PVSSn.n:
            print("人数过多")
        else:
            for i in party:
                d = Zp_Group.Number_in_Zp(1, PVSSn.q)
                xi = Zp_Group.Number_in_Zp(i, PVSSn.q)
                for j in party:
                    xj = Zp_Group.Number_in_Zp(j, PVSSn.q)
                    if xj != xi:
                        d *= xj // (xj - xi)
                s_re *= Zp_Group.Number_in_Zp(int(PVSSn.member_secrets[i - 1][people - 1]) ** int(d), PVSSn.p)
        return s_re

    def get_NIZK_proof(self):
        return self.NIZK_proof

    def get_key(self):
        return PVSSn.pub_key

    """
    def output(self):

        print("sec:")
        for i in range(PVSSn.n):
            for j in range(PVSSn.n):
                print(PVSSn.member_secrets[i][j], end=" ")
            print("")

        print("r:")
        for i in range(0, PVSSn.n):
            for j in range(PVSSn.n):
                print(PVSSn.ri[i][j], end=" ")
            print("")

        print("HY:")
        for i in range(0, PVSSn.n):
            for j in range(PVSSn.n):
                print(PVSSn.HY[i][j], end=" ")
            print("")

        print("a1:")
        for i in range(0, PVSSn.n):
            for j in range(PVSSn.n):
                print(PVSSn.a1[i][j], end=" ")
            print("")

        print("a2:")
        for i in range(0, PVSSn.n):
            for j in range(PVSSn.n):
                print(PVSSn.a2[i][j], end=" ")
            print("")

        print("chg:")
        for i in range(PVSSn.n):
            print(PVSSn.chg[i], end=" ")
        print("")

        print("pri:")
        for i in range(PVSSn.n):
            print(PVSSn.pri_key[i], end=" ")
        print("")

        print("pub:")
        for i in range(PVSSn.n):
            print(PVSSn.pub_key[i], end=" ")
        print("")
        """


"""
receive = []
pty = [1, 2, 4]

p1 = PVSSn(5, 3)
p1.Generate(1)
p2 = PVSSn(5, 3)
p2.Generate(2)
p3 = PVSSn(5, 3)
p3.Generate(3)
p4 = PVSSn(5, 3)
p4.Generate(4)
p5 = PVSSn(5, 3)
 #Generate可以用于重新选择秘密
p5.Generate(5)
print(p1.Share_Verify(1))
print(p1.Reconstruct(1, pty))
print(p1.get_secret())
p1.Generate(1)
print(p1.Share_Verify(1))
print(p1.Reconstruct(1, pty))
print(p1.Share_Verify(1))
print(p1.get_secret())

print(p1.share_dec_verify(5, 3))
"""
