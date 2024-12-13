import VRFn
import random
import NumberTheory as NT


class VRFn_Dist:
    p = VRFn.VRFn.PRIME
    q = VRFn.VRFn.q
    g = VRFn.VRFn.g
    Scrts = None
    t = None
    n = None
    participants = None
    func_value = None
    SKs = None
    PKs = None
    v = None
    vsb = None

    def __init__(self, n, t):

        VRFn_Dist.n = n
        VRFn_Dist.t = t
        VRFn_Dist.participants = [None] * VRFn_Dist.n
        VRFn_Dist.Scrts = [None] * VRFn_Dist.n
        VRFn_Dist.SKs = [0] * VRFn_Dist.n
        VRFn_Dist.PKs = [0] * VRFn_Dist.n
        VRFn_Dist.v = [0] * VRFn_Dist.n
        VRFn_Dist.vsb = [[None] * VRFn_Dist.n] * VRFn_Dist.n
        for i in range(n):
            VRFn_Dist.participants[i] = VRFn.VRFn()

    def DistKG_init(self):
        for i in range(VRFn_Dist.n):
            SK, PK = VRFn_Dist.participants[i].Keygen()
            VRFn_Dist.Scrts[i] = (SK, PK)

    def DistKG_deal(self, slf_idx, t, alpha):
        """

        :param slf_idx: 调用者编号，从1开始
        :param t:门限值
        :param alpha:
        :return:
        """
        slf_idx -= 1
        self.a_p = [[0] * t] * VRFn_Dist.n
        VRFn_Dist.func_value = [[0] * VRFn_Dist.n] * VRFn_Dist.n

        self.a_p[slf_idx][0] = VRFn_Dist.Scrts[slf_idx][1]
        for i in range(1, t):
            self.a_p[slf_idx][i] = random.randint(1, VRFn_Dist.q - 1)  # 多项式系数

        for i in range(1, VRFn_Dist.n + 1):  # 计算每个节点的
            tmp = 0
            for j in range(VRFn_Dist.t):  # 计算t-1次多项式
                tmp = (tmp + (self.a_p[slf_idx][j] % VRFn_Dist.p * pow(i, j, VRFn_Dist.p)) % VRFn_Dist.p) % VRFn_Dist.p
            VRFn_Dist.func_value[slf_idx][j] = tmp
        for i in range(VRFn_Dist.n):
            if i == slf_idx:
                continue
            else:
                VRFn_Dist.SKs[slf_idx] = (VRFn_Dist.SKs[slf_idx] + VRFn_Dist.func_value[slf_idx][
                    i] % VRFn_Dist.p) % VRFn_Dist.p
        VRFn_Dist.PKs[slf_idx] = pow(VRFn_Dist.g, VRFn_Dist.SKs[slf_idx], VRFn_Dist.p)
        return

    def PartialEval(self, alpha, SK, slf_idx):
        slf_idx -= 1
        v = pow(NT.Hash(NT.decToOctet(alpha)), SK, VRFn_Dist.p)
        for i in range(VRFn_Dist.n):
            pi, beta = VRFn_Dist.participants[i].Hashing(NT.decToOctet(alpha), SK)
            si = (i, v, pi)
            VRFn_Dist.vsb[slf_idx][i] = (v, si, beta)
        return

    def combine(self, alpha, slf_idx):
        slf_idx -= 1
        R = 0
        pi_lst = []
        """
        for i in range(VRFn_Dist.n):
            VRFn.VRFn.Verify(NT.decToOctet(alpha), VRFn_Dist.PKs, VRFn_Dist.vsb[slf_idx][i][1][2][0], VRFn_Dist.vsb[slf_idx][i][1][2][1],
                           VRFn_Dist.vsb[slf_idx][i][1][2][2])
        """
        for i in range(VRFn_Dist.n):
            R = R + VRFn_Dist.vsb[i][slf_idx][2]
            pi_lst.append(VRFn_Dist.vsb[i][slf_idx][1])

        pi = tuple(pi_lst)

        return R, pi

    def Verify(self, alpha, slf_idx, VRFny_idx, R, pi):
        slf_idx -= 1
        Rtmp = 0
        pi_lst = []
        VRFn.VRFn.Verify(NT.decToOctet(alpha), VRFn_Dist.PKs, VRFn_Dist.vsb[slf_idx][VRFny_idx][1][2][0],
                       VRFn_Dist.vsb[slf_idx][VRFny_idx][1][2][1],
                       VRFn_Dist.vsb[slf_idx][VRFny_idx][1][2][2])

        for i in range(VRFn_Dist.n):
            R = R + VRFn_Dist.vsb[i][slf_idx][2]
            pi_lst.append(VRFn_Dist.vsb[i][slf_idx][1])

        pitmp = tuple(pi_lst)

        if R == Rtmp and pi == pitmp:
            return True
        else:
            return False

    def Reconstruc(self, alpha, t, slf_idx, party=[]):
        slf_idx -= 1
        SK_dot = 0
        beta_j = 0
        pi_j = []
        for i in range(VRFn_Dist.n):
            SK_dot = (SK_dot + VRFn_Dist.func_value[slf_idx][i]) % VRFn_Dist.p

        for i in range(VRFn_Dist.n):
            if i in party:
                beta = VRFn_Dist.vsb[slf_idx][i][2]
                pi = VRFn_Dist.vsb[slf_idx][i][1][2]
            else:
                beta, pi = VRFn.VRFn.Hashing(NT.decToOctet(alpha), SK_dot)

            pi_j.append(pi)
            beta_j = (beta + beta_j) % VRFn_Dist.p

        return beta_j, pi_j

