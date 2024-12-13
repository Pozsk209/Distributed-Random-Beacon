import VRF
import VRF_Dist
from VRF_Dist import *
import random
import NumberTheory as NT
import hashlib

class VRF_Chain:

    alpha = 0


    def __init__(self, n, t):
        self.n = n
        self.t = t
        self.blocks = []
        self.hr = hashlib.sha256()
        self.VRFuse = VRF_Dist(n, t)
        self.VRFuse.DistKG_init()
        VRF_Chain.alpha = random.randint(1, VRF_Dist.q)
        for i in range(1, n+1):
            self.VRFuse.DistKG_deal(i, t, VRF_Chain.alpha)
        for i in range(1, n+1):
            self.VRFuse.PartialEval(VRF_Chain.alpha, VRF_Dist.SKs[i-1], i)

    def __iter__(self):
        self.index = 0
        R0_hash = hashlib.sha256()
        for i in range(1, self.n+1):
            Rtmp, pi = self.VRFuse.combine(VRF_Chain.alpha, i)
            R0_hash.update(str(Rtmp).encode("UTF-8"))
        self.R = R0_hash.hexdigest()
        self.blocks.append(
            {
                "Index": self.index,
                "Random Value": self.R,
                "Block Type": "Initial",
                "Prev L-Block Hash": None,
                "R-Block HashList": None,
                "Old secret": None,
                "New Com": None,
                "C": None,
                "Sign": None
            })
        return self

    def __next__(self):
        R_Blk_HashList = []
        for i in (self.index, -1, -1):
            hb = hashlib.sha256(str(self.blocks[i]).encode("UTF-8"))  # 应当检查block类型
            if self.blocks[i]["Block Type"] != "Recovered":
                prev_L_Block = hb.hexdigest()
                break
            else:
                R_Blk_HashList.append(hb.hexdigest())


        Li = random.randint(1, self.n+1)

        need_re = False
        party = [0] * self.t
        for i in range(self.t):
            party[i] = random.randint(1, self.n+1) # t位恢复者

        if not need_re:
            old_s = self.R
            tmps, pi = self.VRFuse.combine(NT.decToOctet(int(old_s, 16)), Li-1)
            self.hr.update(str(tmps).encode("UTF-8"))
            self.R = self.hr.hexdigest()
            self.index += 1


            signiture = hashlib.sha256(("Index" + str(self.index) + "Random Value" + str(self.R) + "Block TypeLeader" +
                                        "Prev L-Block Hash" + str(prev_L_Block) + "R-Block HashList" + str(
                        R_Blk_HashList) +
                                        "Old secret" + str(old_s) + "New Com"  + "C").encode("UTF-8"))
            self.blocks.append(
                {
                    "Index": self.index,
                    "Random Value": self.R,
                    "Block Type": "Leader",
                    "Prev L-Block Hash": prev_L_Block,
                    "R-Block HashList": R_Blk_HashList,
                    "Old secret": old_s,
                    "New Com": None,
                    "C": None,  # 这个部分存在问题，写完别的再来探讨
                    "Sign": signiture.hexdigest()
                })

    def get_block(self, n):
        return self.blocks[n]