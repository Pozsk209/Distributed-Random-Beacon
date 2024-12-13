import Schnorr_Group as SG
import socket
import threading

"""
直接在GUI界面手动输入用户的ip地址和用户名，并据此建立list
"""


Zp = SG.SchnorrGroup(4)

print(Zp.q)
print(Zp.p)
print(Zp.g)
print("h:", Zp.h)

for i in range(Zp.q):
    print(Zp.getnumber(i))

