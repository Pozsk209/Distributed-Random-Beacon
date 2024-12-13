import random
import Schnorr_Group as SG
import NumberTheory as NT


class VSS_n:
    """
    公布：p,q,r,g,G,公钥，秘密碎片，承诺
    """

    '''
    n = None
    t = None
    uid = None
    pri_key = None
    usr_pub_key = None
    member_commitments = None #需要分发
    member_shares = None # 收到的秘密
    received_secret = None
    other_commitments = None #需要接收
    '''

    def __init__(self, n, t, uid, secure_number):
        """
        初始化，建议在此处分发该实例的p,q,r,g,G
        :param n: 人数
        :param t: 门限值
        """

        self.Gq = SG.SchnorrGroup(secure_number)
        self.p = self.Gq.p
        self.q = self.Gq.q
        self.G = self.Gq.G
        self.g = self.Gq.g
        self.n = n
        self.t = t
        self.uid = uid
        self.a_p = []
        self.a_q = []
        self.member_commitments = []
        self.member_shares = []
        self.other_commitments = [[]] * n
        self.other_p = []
        self.other_q = []
        self.other_g = []
        self.setvalue = False
        for i in range(self.t):
            self.member_shares.append(0)
            #self.other_commitments.append([])
            self.other_p.append(0)
            self.other_q.append(0)
            self.other_g.append(0)

    def secret_chosen(self):
        self.s = self.Gq.getnumber(random.randrange(0, self.q))
        self.a_p.append(self.s)
        self.a_q.append(self.s % self.q)

    def gen_coefficients(self):
        for i in range(1, self.t):
            self.a_p.append(self.Gq.getnumber(random.randrange(0, self.q)))
            self.a_q.append(self.a_p[i] % self.q)

    def f(self, x):
        y = 0
        for i in range(self.t):
            y = (self.a_q[i] * pow(x, i, self.q) + y) % self.q
        return y

    def commitment(self):
        for i in range(self.t):
            self.member_commitments.append(pow(self.g, self.a_q[i], self.p))

    def generate(self):
        VSS.secret_chosen(self)
        VSS.gen_coefficients(self)
        VSS.commitment(self)

    def distribute_secret(self, uid):
        return VSS.f(self, uid) % self.q

    def sendvalue(self):
        return str(self.uid) + ":" + str(self.p) + ":" + str(self.q) + ":" + str(self.g) + ":" + str(self.member_commitments)

    def getvalue(self, other_uid, p, q, g, other_si, other_com=None):
        self.setvalue = True
        other_uid -= 1
        self.member_shares[other_uid] = other_si
        self.other_p[other_uid] = p
        self.other_q[other_uid] = q
        self.other_g[other_uid] = g
        for i in range(self.t):
            self.other_commitments[other_uid].append(other_com[i])

    def is_other_empty(self, other_uid):
        return not self.setvalue

    def prints(self):
        print("s:", self.s)
        print("s%q", self.a_q)

    def verify(self, other_uid):
        """
        验证他人的是否正确，不是自己的
        :param uid:
        :return:
        """
        other_uid -= 1
        left = pow(self.other_g[other_uid], self.member_shares[other_uid], self.other_p[other_uid])
        right = 1
        for i in range(self.t):
            right = pow(self.other_commitments[other_uid][i], pow(self.uid, i, self.other_q[other_uid]),
                        self.other_p[other_uid]) * right % self.other_p[other_uid]
        print(right)
        print(left)
        if left == right:
            return True
        else:
            return False

    def reconstruct(self, q, partyuid=None, partysec=None):
        """

        :param partysec:
        :param partyuid: 其他人的uid，从1开始
        :return:
        """
        num = len(partyuid)
        s_re = 0
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
                        d = (-partyuid[j] * NT.inv_mod(partyuid[i] - partyuid[j], q) % q) * d % q
                s_re = (s_re + (d * partysec[i]) % q) % q
        return s_re % q


p1 = VSS(5, 3, 1, 4)  # 一个程序
p2 = VSS(5, 3, 2, 4)  # 两个程序
p3 = VSS(5, 3, 3, 4)  # 三个程序
p4 = VSS(5, 3, 4, 4)  # 四个程序
p1.generate()
p2.generate()
p3.generate()
p4.generate()

print("p2 com:", p2.member_commitments)
p2.prints()
p1.getvalue(2, p2.p, p2.q, p2.g, p2.distribute_secret(1), p2.member_commitments)  # 接收方
p3.getvalue(2, p2.p, p2.q, p2.g, p2.distribute_secret(3), p2.member_commitments)
p4.getvalue(2, p2.p, p2.q, p2.g, p2.distribute_secret(4), p2.member_commitments)

print("p1<-p2 com:", p1.other_commitments)
print("p1<-p2 s:", p1.member_shares)
print([p2.distribute_secret(1), p2.distribute_secret(3), p2.distribute_secret(4)])
print(p1.verify(2))
print(p2.reconstruct(p2.q, [1, 3, 4], [p2.distribute_secret(1), p2.distribute_secret(3), p2.distribute_secret(4)]))
