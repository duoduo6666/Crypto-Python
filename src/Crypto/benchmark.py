import time
import __init__ as Crypto

class perf:
    def __init__(self):
        self.time = time.perf_counter()
    def __enter__(self):
        pass
    def __exit__(self,exc_type,exc_val,exc_tb):
        print(time.perf_counter()-self.time)

import collision
with perf():
    # for i in ((bytes(range(0x100)) * 0x100)[i:i+8] for i in range(0,0x2000,8)):
    #     Crypto.SHA1(i)
    collision.SHA1(Crypto.SHA1(b"abc"),4,8,8)