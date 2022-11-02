import __init__ as Crypto
import standard
import collision
from signal import signal,SIGINT
from random import randbytes
from time import perf_counter

class perf:
    def __init__(self):
        self.time = perf_counter()
    def __enter__(self):
        pass
    def __exit__(self,exc_type,exc_val,exc_tb):
        print(perf_counter()-self.time)

class size():
    base = {
        0 : "",
        1 : "K",
        2 : "M",
        3 : "G",
        4 : "T",
        5 : "P"
    }
    def __init__(self,size:int):
        self.size = size
    def __to_str(self) -> str:
        t = self.size
        i = 0.
        while t > 128:
            t /= 1024
            i += 1
        return str(round(t,2)) + self.base[i]
    def __repr__(self):
        return self.__to_str()
    def __str__(self):
        return self.__repr__()

if __name__ == "__main__":
    func = {
        "SHA-1":standard.SHA1,
    }
    argv = {
        "SHA-1":(randbytes(56)),
    }
    num = 1024
    def _exit_(signum, frame):
        print("\b\b  \b\b")
        raise SystemExit
    signal(SIGINT,_exit_)
    while True:
        time = perf_counter()
        for _ in range(num):
            standard.SHA1(randbytes(56))
        print(f"\r        \r{size(1/(perf_counter()-time)*num)}H/s",end="")
        

# with perf():
    # for i in ((bytes(range(0x100)) * 0x100)[i:i+8] for i in range(0,0x2000,8)):
    #     Crypto.SHA1(i)
    # collision.SHA1(Crypto.SHA1(b"abc"),4,8,8)