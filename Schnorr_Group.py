import NumberTheory as NT
import math


class SchnorrGroup:
    """

    """
    Zp_star = None
    G = None
    p = None
    q = None
    g = None
    r = None
    h = 2


    def __init__(self, S_Para: int):
        """
        :param S_Para: 安全参数
        """
        self.S_Para = S_Para
        if SchnorrGroup.p is None:
            SchnorrGroup.p, SchnorrGroup.q, SchnorrGroup.r = NT.gen_prime(S_Para)
            SchnorrGroup.h = NT.primitive_root(SchnorrGroup.p, SchnorrGroup.q)
            SchnorrGroup.g = pow(SchnorrGroup.h, SchnorrGroup.r, SchnorrGroup.p)
            SchnorrGroup.G = NT.primitive_root(SchnorrGroup.p, SchnorrGroup.q)#另一个生成元

    def getnumber(self, power: int):
        return NT.power_mod(SchnorrGroup.g, power, SchnorrGroup.p)

    def change(self,p,q,g,G):
        SchnorrGroup.p = p
        SchnorrGroup.q = q
        SchnorrGroup.g = g
        SchnorrGroup.G = G

