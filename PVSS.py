"""
我们初步的思想是每生成一个实例，就为其返回一个唯一的标号
第一个人必须输入总人数n和门限值t。在这个阶段，所有标号会提前约定好，当新生成一个实例时，标号就会分发
然后每个参与者分发的秘密，就根据标号，秘密地分发给其他参与者。可以根据标号（或者实例的id）来确定其是否有资格知晓这个秘密。

后期可以设置重置函数

"""

import random
import Zp_Group
import hashlib



class PVSS:
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
        if PVSS.n is None:
            PVSS.n = n
            PVSS.key_gen(self)

        if PVSS.t is None:
            PVSS.t = t

        self.a_q = [None]*t  # 模q的系数
        self.a_p = [None]*t  # Zp中的系数
        self.alpha = [None]*t
        #self.NIZK_proof = []

        if len(PVSS.member_secrets) == 0:
            PVSS.member_commitments = [[None]*t for i in range(n)]
            PVSS.member_secrets = [[None]*n for i in range(n)]
            PVSS.pi = [[None]*n for i in range(n)]
            PVSS.ri = [[None]*n for i in range(n)]
            PVSS.HX = [[None]*n for i in range(n)]
            PVSS.HY = [[None]*n for i in range(n)]
            PVSS.Hw = [[None]*n for i in range(n)]
            PVSS.a1 = [[None]*n for i in range(n)]
            PVSS.a2 = [[None]*n for i in range(n)]
            PVSS.chg = [None]*n

            for i in range(PVSS.n):
                for j in range(PVSS.n):
                    PVSS.Hw[i][j] = Zp_Group.Number_in_Zp(int(random.choice(PVSS.G)), PVSS.q)
                    PVSS.a1[i][j] = Zp_Group.Number_in_Zp(PVSS.a ** int(PVSS.Hw[i][j]), PVSS.p)
                    PVSS.a2[i][j] = Zp_Group.Number_in_Zp(int(PVSS.pub_key[j]) ** int(PVSS.Hw[i][j]), PVSS.p)

    def key_gen(self):
        """
        生成参与者的公钥和私钥以及私钥的逆
        :return:无
        """
        tmp = Zp_Group.Number_in_Zp(PVSS.a_enc, PVSS.p)
        for i in range(PVSS.n):
            x = random.choice(PVSS.G)
            PVSS.pri_key.append(x)
            x_inv = Zp_Group.Number_in_Zp(1, PVSS.q) // Zp_Group.Number_in_Zp(int(x), PVSS.q)
            PVSS.pri_inv.append(x_inv)
            PVSS.pub_key.append(tmp ** x)
        return

    def secret_chosen(self):
        """
        秘密选择函数，在子群G上随机选择并用公钥加密
        :return: 无
        """
        s = random.choice(PVSS.G)  # 选择的s需要小于q
        #print("s:", s)
        self.a_p[0] = s
        self.a_q[0] = s.change_modulo(PVSS.q)
        self.s = Zp_Group.Number_in_Zp(PVSS.a_enc ** (int(s) % PVSS.q), PVSS.p)

        #print("s:", self.s)
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
        for i in range(1, PVSS.t):
            self.a_p[i] = random.choice(PVSS.G)
            self.a_q[i] = self.a_p[i].change_modulo(PVSS.q)
            #print("a_q:", self.a_q[i])
        return

    def f(self, x):
        """
        f函数计算秘密碎片f(x)
        :param x:x，用于计算f(x)，常使用参与者下标
        :return:f(x)
        """
        tmpx = Zp_Group.Number_in_Zp(x, PVSS.q)
        y = Zp_Group.Number_in_Zp(0, PVSS.q)
        for i in range(PVSS.t):
            y += self.a_q[i] * (tmpx ** i)
        return y

    def Commitment(self, index):
        """
        生成系数的承诺，用于检验碎片的正确性
        :param index:参与方在f函数输入的值，常使用下标，务必与f函数输入参数一致
        :return:无
        """
        tmpa = Zp_Group.Number_in_Zp(PVSS.a, PVSS.p)
        for i in range(PVSS.t):
            self.alpha[i] = tmpa ** self.a_p[i]
            PVSS.member_commitments[index - 1][i] = self.alpha[i]
        return

    def Generate(self, index):  # index是成员的分配的下标 1,2,3,... ,n
        """
        生成或者重新生成，包括随机选择的秘密，多项式系数以及相关的承诺。
        :param index:参与者输入值，通常是下标
        :return:无
        """
        self.shares = []

        # PVSS.key_gen(self)
        PVSS.secret_chosen(self)
        PVSS.gen_coefficients(self)  # 说明每个人的多项式不一样
        ag = Zp_Group.Number_in_Zp(PVSS.a, PVSS.p)
        for i in range(1, PVSS.n + 1):
            PVSS.pi[index - 1][i - 1] = PVSS.f(self, i)
            pubkey = Zp_Group.Number_in_Zp(int(PVSS.pub_key[i - 1]), PVSS.p)
            #print("pi:", PVSS.pi[index - 1][i - 1])
            #print(PVSS.a_enc ** int(PVSS.pi[index - 1][i - 1]) % PVSS.p)
            PVSS.HX[index - 1][i - 1] = ag.__pow__(int(PVSS.pi[index - 1][i - 1]), PVSS.p)  # 计算X
            PVSS.HY[index - 1][i - 1] = pubkey.__pow__(int(PVSS.pi[index - 1][i - 1]), PVSS.p)  # 计算Y 实际就是要公开的秘密
            # PVSS.ri[index - 1][i] = PVSS.Hw[index - 1][i] - pi*

            # PVSS.member_secrets[index - 1].append(PVSS.HY[index - 1][i - 1])  # 压入公共列表
            # print("shares:", self.shares[i - 1])
        PVSS.Commitment(self, index)  # 计算验证参数

        # ----------Hash----------------
        Hashtmp = hashlib.sha256()
        strHash = ""
        strHX = ""
        strHY = ""
        stra1 = ""
        stra2 = ""
        for i in range(PVSS.n):
            strHX += str(PVSS.HX[index - 1][i])
            strHY += str(PVSS.HY[index - 1][i])
            stra1 += str(PVSS.a1[index - 1][i])
            stra2 += str(PVSS.a2[index - 1][i])
        strHash = strHX + strHY + stra1 + stra2
        #print("strhash", strHash)
        Hashtmp.update(strHash.encode("UTF-8"))
        PVSS.chg[index - 1] = Zp_Group.Number_in_Zp(int(Hashtmp.hexdigest(), 16), PVSS.p)  # challenge

        for i in range(PVSS.n):
            pichg = Zp_Group.Number_in_Zp(int(PVSS.pi[index - 1][i]) * int(PVSS.chg[index - 1]), PVSS.q)
            PVSS.ri[index - 1][i] = PVSS.Hw[index - 1][i] - pichg

        self.NIZK_proof = ([int(i) for i in PVSS.member_commitments[index - 1]],int(PVSS.chg[index - 1]), [int(i) for i in PVSS.ri[index - 1]])
        #return self.alpha
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
        tmpa = Zp_Group.Number_in_Zp(1, PVSS.p)
        tmpg = PVSS.HX[leader_idx - 1][self_idx - 1]
        for i in range(PVSS.t):
            # tmpa = tmpa * (self.alpha[i] ** (j ** i))
            tmpa = tmpa * (PVSS.member_commitments[leader_idx - 1][i] ** (self_idx ** i))
        print(tmpg)
        print(tmpa) #要把tmpa放入hash中对比
        '''
        for j in range(1, PVSS.n + 1):
            tmpa = Zp_Group.Number_in_Zp(1, PVSS.p)
            for i in range(PVSS.t):
                # tmpa = tmpa * (self.alpha[i] ** (j ** i))
                tmpa = tmpa * (PVSS.member_commitments[leader_idx - 1][i] ** (j ** i))
            tmp_hash.update(str(tmpa).encode("UTF-8"))

        for j in range(PVSS.n):
            tmp_hash.update(str(PVSS.HY[leader_idx - 1][j]).encode("UTF-8"))

        for j in range(1, PVSS.n + 1):

            gr = Zp_Group.Number_in_Zp(int(PVSS.a) ** int(PVSS.ri[leader_idx - 1][j - 1]), PVSS.p)
            # print("gr", gr)
            xc = Zp_Group.Number_in_Zp(int(PVSS.HX[leader_idx - 1][j - 1]) ** int(PVSS.chg[leader_idx - 1]), PVSS.p)
            # print("xc", xc)
            tmpa1 = gr * xc
            tmp_hash.update(str(tmpa1).encode("UTF-8"))
            #print('tmpa1', tmpa1)

        """
        yr = Zp_Group.Number_in_Zp(int(PVSS.pub_key[leader_idx - 1]) ** int(PVSS.ri[leader_idx - 1][self_idx - 1]),
                                   PVSS.p)
        # print("yr", yr)
        yc = Zp_Group.Number_in_Zp(int(PVSS.HY[leader_idx - 1][self_idx - 1]) ** int(PVSS.chg[leader_idx - 1]), PVSS.p)
        # print("yc", yc)
        tmpa2 = yr * yc
        tmp_hash.update(str(tmpa2).encode("UTF-8"))
        print('tmpa2', tmpa2)"""

        for j in range(1, PVSS.n + 1):
            yr = Zp_Group.Number_in_Zp(int(PVSS.pub_key[j - 1]) ** int(PVSS.ri[leader_idx - 1][j - 1]),
                                       PVSS.p)
            # print("yr", yr)
            yc = Zp_Group.Number_in_Zp(int(PVSS.HY[leader_idx - 1][j - 1]) ** int(PVSS.chg[leader_idx - 1]), PVSS.p)
            # print("yc", yc)
            tmpa2 = yr * yc
            tmp_hash.update(str(tmpa2).encode("UTF-8"))
            #print('tmpa2', tmpa2)

        num_tmp_hash = Zp_Group.Number_in_Zp(int(tmp_hash.hexdigest(), 16), PVSS.p)

        #print('numhash', num_tmp_hash)

        if num_tmp_hash == PVSS.chg[leader_idx - 1]:
            return True
        else:
            return False

    def share_decrypt(self):
        """
        碎片解密，用于恢复随机数
        :return:无
        """
        for i in range(PVSS.n):
            for j in range(PVSS.n):
                PVSS.member_secrets[i][j] = Zp_Group.Number_in_Zp(int(PVSS.HY[i][j]) ** int(PVSS.pri_inv[j]), PVSS.p)
                # 注意一下priinv是i还是j

        return

    def share_dec_verify(self, leader_idx, self_idx):
        """
        :param leader_idx: 秘密对应的leader
        :param self_idx: 验证者，理论上验证一个即可
        :return:验证成功或者失败
        """
        PVSS.share_decrypt(self)
        tmpr = Zp_Group.Number_in_Zp(int(PVSS.Hw[leader_idx - 1][self_idx - 1]) - int(PVSS.pri_key[self_idx - 1]) * int(PVSS.chg[self_idx - 1]), PVSS.q)
        dv_Hash = hashlib.sha256()
        tmp_Hash = hashlib.sha256()
        H_str = str(PVSS.pub_key[self_idx-1]) + str(PVSS.HY[leader_idx - 1][self_idx - 1]) +str(Zp_Group.Number_in_Zp(int(PVSS.a_enc) ** int(PVSS.Hw[leader_idx - 1][self_idx - 1]), PVSS.p)) + str(Zp_Group.Number_in_Zp(int(PVSS.member_secrets[leader_idx - 1][self_idx - 1]) ** int(PVSS.Hw[leader_idx - 1][self_idx - 1]), PVSS.p))
        dv_Hash.update(H_str.encode("UTF-8"))
        #print(dv_Hash.hexdigest())
        Gr = Zp_Group.Number_in_Zp(int(PVSS.a_enc) ** int(tmpr), PVSS.p)
        yc = Zp_Group.Number_in_Zp(int(PVSS.pub_key[self_idx - 1]) ** int(PVSS.chg[self_idx - 1]), PVSS.p)
        tmpa1 = Gr * yc

        Sr = Zp_Group.Number_in_Zp(int(PVSS.member_secrets[leader_idx - 1][self_idx - 1]) ** int(tmpr), PVSS.p)
        Yc = Zp_Group.Number_in_Zp(int(PVSS.HY[leader_idx - 1][self_idx - 1]) ** int(PVSS.chg[self_idx - 1]), PVSS.p)
        tmpa2 = Sr * Yc
        H_tmp = str(PVSS.pub_key[self_idx-1]) + str(PVSS.HY[leader_idx - 1][self_idx - 1]) +str(tmpa1) + str(tmpa2)
        tmp_Hash.update(H_tmp.encode("UTF-8"))
        #print("H_str", H_str)
        #print("H_tmp", H_tmp)

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
        PVSS.share_decrypt(self)
        num = len(party)
        s_re = Zp_Group.Number_in_Zp(1, PVSS.p)
        if num < PVSS.t:
            print("参与者人数需多于门限值")
        elif num > PVSS.n:
            print("人数过多")
        else:
            for i in party:
                d = Zp_Group.Number_in_Zp(1, PVSS.q)
                xi = Zp_Group.Number_in_Zp(i, PVSS.q)
                for j in party:
                    xj = Zp_Group.Number_in_Zp(j, PVSS.q)
                    if xj != xi:
                        d *= xj // (xj - xi)
                s_re *= Zp_Group.Number_in_Zp(int(PVSS.member_secrets[people - 1][i - 1]) ** int(d), PVSS.p)
        return s_re

    def get_NIZK_proof(self):
        return self.NIZK_proof

    def get_key(self):
        return PVSS.pub_key

    """
    def output(self):
        
        print("sec:")
        for i in range(PVSS.n):
            for j in range(PVSS.n):
                print(PVSS.member_secrets[i][j], end=" ")
            print("")

        print("r:")
        for i in range(0, PVSS.n):
            for j in range(PVSS.n):
                print(PVSS.ri[i][j], end=" ")
            print("")

        print("HY:")
        for i in range(0, PVSS.n):
            for j in range(PVSS.n):
                print(PVSS.HY[i][j], end=" ")
            print("")

        print("a1:")
        for i in range(0, PVSS.n):
            for j in range(PVSS.n):
                print(PVSS.a1[i][j], end=" ")
            print("")

        print("a2:")
        for i in range(0, PVSS.n):
            for j in range(PVSS.n):
                print(PVSS.a2[i][j], end=" ")
            print("")

        print("chg:")
        for i in range(PVSS.n):
            print(PVSS.chg[i], end=" ")
        print("")

        print("pri:")
        for i in range(PVSS.n):
            print(PVSS.pri_key[i], end=" ")
        print("")

        print("pub:")
        for i in range(PVSS.n):
            print(PVSS.pub_key[i], end=" ")
        print("")
        """

"""
receive = []
pty = [1, 2, 4]

p1 = PVSS(5, 3)
p1.Generate(1)
p2 = PVSS(5, 3)
p2.Generate(2)
p3 = PVSS(5, 3)
p3.Generate(3)
p4 = PVSS(5, 3)
p4.Generate(4)
p5 = PVSS(5, 3)
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
