import VSS_Random_Beacon_chain as VSS
import PVSS_Random_Beacon_Chain as PVSS
import PVSSn_Random_Beacon_Chain as PVSSn
import VRF_Random_Beacon_Chain as VRF
import VRFn_Random_Beacon_Chain as VRFn
import time

def VSS_Gen(n, t):
    test = VSS.VSS_chain(n, t)
    T1 = time.perf_counter()
    niter = iter(test)
    T2 = time.perf_counter()
    i = 0
    while True:
        #p = next(niter)
        i = yield test.get_block(i), test.get_block(i)['Random'], (T2 - T1) * 1000000
        T1 = time.perf_counter()
        next(niter)
        T2 = time.perf_counter()

def PVSS_Gen(n, t):
    test = PVSS.PVSS_chain(n, t)
    T1 = time.perf_counter()
    niter = iter(test)
    T2 = time.perf_counter()
    i = 0
    while True:
        #p = next(niter)
        i = yield test.get_block(i), test.get_block(i)['Random Value'], (T2 - T1) * 1000000
        T1 = time.perf_counter()
        next(niter)
        T2 = time.perf_counter()

def PVSSn_Gen(n, t):
    test = PVSSn.PVSSn_chain(n, t)
    T1 = time.perf_counter()
    niter = iter(test)
    T2 = time.perf_counter()
    i = 0
    while True:
        #p = next(niter)
        i = yield test.get_block(i), test.get_block(i)['Random Value'], (T2 - T1) * 1000000
        T1 = time.perf_counter()
        next(niter)
        T2 = time.perf_counter()

def VRF_Gen(n, t):
    test = VRF.VRF_Chain(n, t)
    T1 = time.perf_counter()
    niter = iter(test)
    T2 = time.perf_counter()
    i = 0
    while True:
        #p = next(niter)
        i = yield test.get_block(i), test.get_block(i)['Random Value'], (T2 - T1) * 1000000
        T1 = time.perf_counter()
        next(niter)
        T2 = time.perf_counter()

def VRFn_Gen(n, t):
    test = VRFn.VRFn_Chain(n, t)
    T1 = time.perf_counter()
    niter = iter(test)
    T2 = time.perf_counter()
    i = 0
    while True:
        #p = next(niter)
        i = yield test.get_block(i), test.get_block(i)['Random Value'], (T2 - T1) * 1000000
        T1 = time.perf_counter()
        next(niter)
        T2 = time.perf_counter()


def VSS_Random_Beacon(n, t):
    while True:
        yield from VSS_Gen(n, t)

def PVSS_Random_Beacon(n, t):
    while True:
        yield from PVSS_Gen(n, t)

def PVSS_n_Random_Beacon(n, t):
    while True:
        yield from PVSSn_Gen(n, t)

def VRF_Random_Beacon(n, t):
    while True:
        yield from VRF_Gen(n, t)

def VRF_n_Random_Beacon(n, t):
    while True:
        yield from VRFn_Gen(n, t)


