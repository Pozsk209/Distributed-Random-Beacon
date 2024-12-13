import VRF
import random
import NumberTheory as NT


class VRF_Dist:
    p = VRF.VRF.PRIME
    q = VRF.VRF.q
    g = VRF.VRF.g
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

        VRF_Dist.n = n
        VRF_Dist.t = t
        VRF_Dist.participants = [None] * VRF_Dist.n
        VRF_Dist.Scrts = [None] * VRF_Dist.n
        VRF_Dist.SKs = [0] * VRF_Dist.n
        VRF_Dist.PKs = [0] * VRF_Dist.n
        VRF_Dist.v = [0] * VRF_Dist.n
        VRF_Dist.vsb = [[None] * VRF_Dist.n] * VRF_Dist.n
        for i in range(n):
            VRF_Dist.participants[i] = VRF.VRF()

    def DistKG_init(self):
        for i in range(VRF_Dist.n):
            SK, PK = VRF_Dist.participants[i].Keygen()
            VRF_Dist.Scrts[i] = (SK, PK)

    def DistKG_deal(self, slf_idx, t, alpha):
        """

        :param slf_idx: 调用者编号，从1开始
        :param t:门限值
        :param alpha:
        :return:
        """
        slf_idx -= 1
        self.a_p = [[0] * t] * VRF_Dist.n
        VRF_Dist.func_value = [[0] * VRF_Dist.n] * VRF_Dist.n

        self.a_p[slf_idx][0] = VRF_Dist.Scrts[slf_idx][1]
        for i in range(1, t):
            self.a_p[slf_idx][i] = random.randint(1, VRF_Dist.q - 1)  # 多项式系数

        for i in range(1, VRF_Dist.n + 1):  # 计算每个节点的
            tmp = 0
            for j in range(VRF_Dist.t):  # 计算t-1次多项式
                tmp = (tmp + (self.a_p[slf_idx][j] % VRF_Dist.p * pow(i, j, VRF_Dist.p)) % VRF_Dist.p) % VRF_Dist.p
            VRF_Dist.func_value[slf_idx][j] = tmp
        for i in range(VRF_Dist.n):
            if i == slf_idx:
                continue
            else:
                VRF_Dist.SKs[slf_idx] = (VRF_Dist.SKs[slf_idx] + VRF_Dist.func_value[slf_idx][
                    i] % VRF_Dist.p) % VRF_Dist.p
        VRF_Dist.PKs[slf_idx] = pow(VRF_Dist.g, VRF_Dist.SKs[slf_idx], VRF_Dist.p)
        return

    def PartialEval(self, alpha, SK, slf_idx):
        slf_idx -= 1
        v = pow(NT.Hash(NT.decToOctet(alpha)), SK, VRF_Dist.p)
        for i in range(VRF_Dist.n):
            pi, beta = VRF_Dist.participants[i].Hashing(NT.decToOctet(alpha), SK)
            si = (i, v, pi)
            VRF_Dist.vsb[slf_idx][i] = (v, si, beta)
        return

    def combine(self, alpha, slf_idx):
        slf_idx -= 1
        R = 0
        pi_lst = []
        """
        for i in range(VRF_Dist.n):
            VRF.VRF.Verify(NT.decToOctet(alpha), VRF_Dist.PKs, VRF_Dist.vsb[slf_idx][i][1][2][0], VRF_Dist.vsb[slf_idx][i][1][2][1],
                           VRF_Dist.vsb[slf_idx][i][1][2][2])
        """
        for i in range(VRF_Dist.n):
            R = R + VRF_Dist.vsb[i][slf_idx][2]
            pi_lst.append(VRF_Dist.vsb[i][slf_idx][1])

        pi = tuple(pi_lst)

        return R, pi

    def Verify(self, alpha, slf_idx, vrfy_idx, R, pi):
        slf_idx -= 1
        Rtmp = 0
        pi_lst = []
        VRF.VRF.Verify(NT.decToOctet(alpha), VRF_Dist.PKs, VRF_Dist.vsb[slf_idx][vrfy_idx][1][2][0],
                       VRF_Dist.vsb[slf_idx][vrfy_idx][1][2][1],
                       VRF_Dist.vsb[slf_idx][vrfy_idx][1][2][2])

        for i in range(VRF_Dist.n):
            R = R + VRF_Dist.vsb[i][slf_idx][2]
            pi_lst.append(VRF_Dist.vsb[i][slf_idx][1])

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
        for i in range(VRF_Dist.n):
            SK_dot = (SK_dot + VRF_Dist.func_value[slf_idx][i]) % VRF_Dist.p

        for i in range(VRF_Dist.n):
            if i in party:
                beta = VRF_Dist.vsb[slf_idx][i][2]
                pi = VRF_Dist.vsb[slf_idx][i][1][2]
            else:
                beta, pi = VRF.VRF.Hashing(NT.decToOctet(alpha), SK_dot)

            pi_j.append(pi)
            beta_j = (beta + beta_j) % VRF_Dist.p

        return beta_j, pi_j

