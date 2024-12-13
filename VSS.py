"""
我们初步的思想是每生成一个实例，就为其返回一个唯一的标号
第一个人必须输入总人数n和门限值t。在这个阶段，所有标号会提前约定好，当新生成一个实例时，标号就会分发
然后每个参与者分发的秘密，就根据标号，秘密地分发给其他参与者。可以根据标号（或者实例的id）来确定其是否有资格知晓这个秘密。

后期可以设置重置函数

"""
import random
import Zp_Group




class VSS:
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

    pri_key = []

    pub_key = []


    def __init__(self, n, t):
        if VSS.n is None:
            VSS.n = n
        if VSS.t is None:
            VSS.t = t
        self.a_q = []  # 模q的系数
        self.a_p = []  # Zp中的系数
        self.alpha = []
        for i in range(VSS.n):
            VSS.member_secrets.append([])
            VSS.member_commitments.append([])

    def key_gen(self):
        tmp = Zp_Group.Number_in_Zp(VSS.a_enc, VSS.p)
        for i in range(VSS.n):
            x = random.choice(VSS.G)
            VSS.pri_key.append(x)
            VSS.pub_key.append(tmp ** x)


    def secret_chosen(self):
        self.s = random.choice(VSS.G)  # 选择的s需要小于q
        self.a_p.append(self.s)
        self.a_q.append(self.s.change_modulo(VSS.q))
        #print("s:", self.s)
        # return self.s

    def gen_coefficients(self):
        for i in range(1, VSS.t):
            self.a_p.append(random.choice(VSS.G))
            self.a_q.append(self.a_p[i].change_modulo(VSS.q))
            # print("a_q:", self.a_q[i])

    def f(self, x):
        tmpx = Zp_Group.Number_in_Zp(x, VSS.q)
        y = Zp_Group.Number_in_Zp(0, VSS.q)
        for i in range(VSS.t):
            y += self.a_q[i] * (tmpx ** i)
        return y

    def Commitment(self, index):
        tmpa = Zp_Group.Number_in_Zp(VSS.a, VSS.p)
        for i in range(VSS.t):
            self.alpha.append(tmpa ** self.a_p[i])
            VSS.member_commitments[index - 1].append(self.alpha[i])

    def Generate(self, index):
        """
        index是成员的分配的下标 1,2,3,... ,n
        """

        self.shares = []

        VSS.secret_chosen(self)
        VSS.gen_coefficients(self)
        for i in range(1, VSS.n + 1):
            self.shares.append(VSS.f(self, i))  # 将秘密分享，以后可以考虑开辟二维列表
            VSS.member_secrets[index - 1].append(self.shares[i - 1])  # 压入公共列表
            # print("shares:", self.shares[i - 1])
        VSS.Commitment(self, index)  # 计算验证参数

        #return self.alpha

    def Verify(self, leader_idx, self_idx):
        """
        验证自己self获得的来自分发者leader的碎片s的正确性。
        :param leader_idx: 密钥碎片发出者的下标，从1开始
        :param self_idx: 自己的下标，从1开始
        :return:s是否正确
        """

        tmpa = Zp_Group.Number_in_Zp(1, VSS.p)
        # tmpg = Zp_Group.Number_in_Zp(VSS.a, VSS.p)
        # tmpg = self.shares[j - 1].__rpow__(VSS.a, VSS.p)
        tmpg = VSS.member_secrets[leader_idx - 1][self_idx - 1].__rpow__(VSS.a, VSS.p)
        for i in range(VSS.t):
            # tmpa = tmpa * (self.alpha[i] ** (j ** i))
            tmpa = tmpa * (VSS.member_commitments[leader_idx - 1][i] ** (self_idx ** i))
        # print(tmpg)
        # print(tmpa)
        if tmpa == tmpg:
            return True
        else:
            return False

    def Reconstruct(self, party=None):
        """
        :param party: 一个列表，表示要执行秘密重建的人的标号
        :return:  秘密值
        """
        num = len(party)
        s_re = Zp_Group.Number_in_Zp(0, VSS.q)
        if num < VSS.t:
            print("参与者人数需多于门限值")
        elif num > VSS.n:
            print("人数过多")
        else:
            for i in party:
                d = Zp_Group.Number_in_Zp(1, VSS.q)
                xi = Zp_Group.Number_in_Zp(i, VSS.q)
                for j in party:
                    xj = Zp_Group.Number_in_Zp(j, VSS.q)
                    if xj != xi:
                        d *= -xj // (xi - xj)
                s_re += d * self.shares[i - 1]
        return s_re

    def get_src(self):
        return self.s

"""
receive = []
pty = [1, 2, 4]

ppp = []

for i in range(5):
    ppp.append(VSS(5,3))
    receive.append(ppp[i].Generate(i+1))


p1 = VSS(5, 3)
p2 = VSS(5, 2)
p3 = VSS(5, 3)
p4 = VSS(5, 3)
p5 = VSS(5, 3)
receive.append(p1.Generate(1))
receive.append(p2.Generate(2))
receive.append(p3.Generate(3))
receive.append(p4.Generate(4))
receive.append(p5.Generate(5))

print(ppp[0].Verify(2, 3))
print(ppp[0].Reconstruct(pty))
'''ppp[0].key_gen()'''
"""