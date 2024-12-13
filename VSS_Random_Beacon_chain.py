"""
每个块包含的内容：
index(块的标号)
上一块的Hash
类型(恢复块还是领导块)
随机数R
"""
import VSS
import hashlib
import random


class VSS_chain:

    blocks = []
    participants = []
    def __init__(self, n, t):
        self.n = n
        self.t = t
        for i in range(0, self.n):
            VSS_chain.participants.append(VSS.VSS(self.n, self.t))
            VSS_chain.participants[i].Generate(i+1)

    def __iter__(self):
        h = hashlib.sha256("3.141592653589".encode("UTF-8"))
        self.a = None
        self.index = 0
        self.R = h.hexdigest()
        VSS_chain.blocks.append({"Index": self.index, "Prev_hash": None, "Block_type": "Initial", "Random": self.R})

        return self

    def __next__(self):

        hb = hashlib.sha256(str(VSS_chain.blocks[self.index]).encode("UTF-8"))
        hr = hashlib.sha256()
        prev_hash = hb.hexdigest()

        leader_index = random.randint(1, self.n)
        party = [1, 2, 4]
        need_re = False
        for person in party:
            if not VSS_chain.participants[person].Verify(leader_index, person):
                need_re = True
                break

        if not need_re:
            s = str(VSS_chain.blocks[self.index]["Random"]) + str(VSS_chain.participants[leader_index-1].get_src())
            hr.update(s.encode("UTF-8"))
            self.R = hr.hexdigest()
            self.index += 1
            VSS_chain.blocks.append({"Index": self.index, "Prev_hash": prev_hash, "Block_type": "Leader", "Random": self.R})
        else:
            s = str(VSS_chain.blocks[self.index]["Random"]) + str(VSS_chain.participants[leader_index-1].Reconstruct(party))
            hr.update(s.encode("UTF-8"))
            self.R = hr.hexdigest()
            self.index += 1
            VSS_chain.blocks.append({"Index": self.index, "Prev_hash": prev_hash, "Block_type": "Recovered", "Random": self.R})

        return VSS_chain.blocks[self.index - 1]["Random"]

    def get_block(self, n):
        #print(VSS_chain.blocks[n])
        return VSS_chain.blocks[n]


"""
test = VSS_chain(5, 3)
niter = iter(test)

for i in range(10):
    tp = input()
    p = next(niter)
    print("第", i, "轮:", p)
    test.get_block(i)
"""