"""


"""
import PVSSn
import hashlib
import random




class PVSSn_chain:

    def __init__(self, n, t):
        self.n = n
        self.t = t
        self.blocks = []
        self.participants = []
        self.ComGs = [None]*self.n
        self.dec_shares = [None]*self.t
        for i in range(0, self.n):
            self.participants.append(PVSSn.PVSSn(self.n, self.t))
            self.participants[i].Generate(i + 1)
        self.pub_key = sorted({i + 1: int(PVSSn.PVSSn.pub_key[i]) for i in range(self.n)}.items(), key=lambda d: d[1],
                              reverse=False)
        #print(self.pub_key)

    def __iter__(self):
        self.index = 0
        R0_hash = hashlib.sha256()
        for i in range(self.n):
            R0_hash.update(str(self.participants[i].get_NIZK_proof()).encode("UTF-8"))
            self.ComGs[i] = self.participants[i].get_NIZK_proof()
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
                "C": self.ComGs,
                "Sign": None
            })
        return self

    def leader_selection(self):
        return self.pub_key[int(str(self.R), 16) % self.n][0] - 1

    def __next__(self):
        R_Blk_HashList = []
        for i in (self.index, -1, -1):
            hb = hashlib.sha256(str(self.blocks[i]).encode("UTF-8"))  # 应当检查block类型
            if self.blocks[i]["Block Type"] != "Recovered":
                prev_L_Block = hb.hexdigest()
                break
            else:
                R_Blk_HashList.append(hb.hexdigest())

        hr = hashlib.sha256()
        Li = PVSSn_chain.leader_selection(self)

        need_re = False
        party = [1, 2, 4]  # t位恢复者

        for person in party:
            if (not self.participants[Li - 1].share_dec_verify(Li+1, person)) or (not self.participants[person - 1].Share_Verify(Li+1)):
                print(self.participants[Li - 1].share_dec_verify(Li+1, person))
                print(self.participants[person - 1].Share_Verify(Li+1))
                need_re = True
                break

        if not need_re:
            Gs = self.participants[Li].get_secret()[0]
            old_s = self.participants[Li].get_secret()[1]
            tmps = str(self.blocks[self.index]["Random Value"]) + str(Gs)
            hr.update(tmps.encode("UTF-8"))
            self.R = hr.hexdigest()
            self.index += 1
            self.participants[Li].Generate(Li + 1)
            self.ComGs[Li] = self.participants[Li].get_NIZK_proof()
            signiture = hashlib.sha256(("Index" + str(self.index) + "Random Value" + str(self.R) + "Block TypeLeader" +
                            "Prev L-Block Hash" + str(prev_L_Block) + "R-Block HashList" + str(R_Blk_HashList) +
                            "Old secret" + str(old_s) + "New Com" + str(self.ComGs[Li]) + "C" + str(self.ComGs)).encode(
                "UTF-8"))
            self.blocks.append(
                {
                    "Index": self.index,
                    "Random Value": self.R,
                    "Block Type": "Leader",
                    "Prev L-Block Hash": prev_L_Block,
                    "R-Block HashList": R_Blk_HashList,
                    "Old secret": old_s,
                    "New Com": self.ComGs[Li],
                    "C": self.ComGs, # 这个部分存在问题，写完别的再来探讨
                    "Sign":signiture.hexdigest()
                })
        else:

            Gs = self.participants[Li].Reconstruct(Li, party)
            tmps = str(self.blocks[self.index]["Random Value"]) + str(Gs)
            hr.update(tmps.encode("UTF-8"))
            for i in range(self.t):
                self.dec_shares[i] = int(PVSSn.PVSSn.member_secrets[Li][party[i]])
            self.index += 1
            self.blocks.append(
                {
                    "Index": self.index,
                    "Random Value": self.R,
                    "Block Type": "Recover",
                    "Decryped Shares": self.dec_shares,
                    "NIZK Dec Verify": None
                })
        return self.blocks[self.index - 1]["Random Value"]



    def get_block(self, n):
        return self.blocks[n]

'''
test = PVSSn_chain(5, 3)
niter = iter(test)

for i in range(10):
    tp = input()
    p = next(niter)
    print("第", i, "轮:", p)
    print(test.get_block(i))
'''