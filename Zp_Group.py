import math
import NumberTheory as NT


class Number_in_Zp():

    def __init__(self, num, modulo):
        self.num = (num + modulo) % modulo
        self.modulo = modulo

    def change_modulo(self,new_modulo):
        return Number_in_Zp((self.num + new_modulo) % new_modulo, new_modulo)
        #我在思考有必要先进行运算吗

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return self.num

    def __add__(self, other):
        return (self.num + other.num) % self.modulo

    def __iadd__(self, other):
        return Number_in_Zp((self.num + other.num) % self.modulo, self.modulo)

    def __sub__(self, other):
        return Number_in_Zp((self.num - other.num) % self.modulo, self.modulo)

    def __mul__(self, other):
        return Number_in_Zp((self.num * other.num) % self.modulo, self.modulo)

    def __imul__(self, other):
        return Number_in_Zp((self.num * other.num) % self.modulo, self.modulo)

    def __floordiv__(self, other):
        inv = NT.inv_mod(other.num, self.modulo)
        return Number_in_Zp((self.num * inv) % self.modulo, self.modulo)

    def __mod__(self, other):
        return self.num % other

    def __rmod__(self, other):
        return other % self.num

    def __pow__(self, power, modulo=None):
        if modulo is None:
            return Number_in_Zp((self.num ** power) % self.modulo, self.modulo)
        else:
            return (self.num ** power) % modulo

    def __int__(self):
        return self.num

    def __rpow__(self, other, modulo=None):
        if modulo is None:
            return Number_in_Zp((other ** self.num) % self.modulo, self.modulo)
        else:
            if type(other) is int:
                return Number_in_Zp((other ** self.num) % modulo, modulo)
            else:
                return Number_in_Zp((other.num ** self.num) % modulo, modulo)

    def __neg__(self):
        return Number_in_Zp((-self.num + self.modulo) % self.modulo,self.modulo)

    def __eq__(self, other):
        return (self.num + self.modulo) % self.modulo == (other.num + self.modulo) % self.modulo

    def __ne__(self, other):
        return (self.num + self.modulo) % self.modulo != (other.num + self.modulo) % self.modulo

    def __lt__(self, other):
        return self.num < other.num

    def __le__(self, other):
        return self.num <= other.num

    def __gt__(self, other):
        return self.num > other.num

    def __ge__(self, other):
        return self.num >= other.num


class Zp_Group:
    """
    数字的下标即为对应数字，因此取数或者运算时从0开始到p-1
    但是切片还是下标从0开始
    """
    Zp_star = None
    G = None
    q = 11
    r = 2
    p = r * q + 1
    g = NT.primitive_root(p, q)
    g_enc = NT.primitive_root(p, q)
    a_enc = g_enc ** r % p
    a = g ** r % p
    # q = random.randrange(2 ** (size - 1), 2 ** size)

    def __init__(self):
        #Zp_Group.p, Zp_Group.q, Zp_Group.r = NT.gen_prime(1024) #生成1024bit的q和p
        if (Zp_Group.Zp_star is None):
            Zp_Group.Zp_star = []
            for i in range(0, Zp_Group.p):
                if math.gcd(i, Zp_Group.p) == 1:
                    Zp_Group.Zp_star.append(Number_in_Zp(i, Zp_Group.p))

        if(Zp_Group.G is None):
            Zp_Group.G = []
            for i in range(0, Zp_Group.q):
                Zp_Group.G.append(Number_in_Zp(Zp_Group.a ** i, Zp_Group.p))
            Zp_Group.G.sort()

        #print("Zp* and G has created successfully!")

        #print("p={}".format(Zp_Group.p))
        #print("q={}".format(Zp_Group.q))
        #print("g={}".format(Zp_Group.g))
        #print("a={}".format(Zp_Group.a))
        #print("aenc={}".format(Zp_Group.a_enc))

    def __getitem__(self, index):
        return Zp_Group.G[index]

    def __setitem__(self, key, value):
        print("操作被禁止！")

    def __contains__(self, item):
        return Zp_Group.G.__contains__(item)

    def __str__(self):
        return Zp_Group.G

    def __index_(self, value):
        return Zp_Group.G.index(value)

    def __len__(self):
        return Zp_Group.q

    def __repr__(self):
        return Zp_Group.G




