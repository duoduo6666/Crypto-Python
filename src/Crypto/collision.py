import __init__ as Crypto
import multiprocessing
import ctypes

from sys import getsizeof

def for_sizeof(sequence,number=False):
    size = 0
    if (type(sequence) is list) or (type(sequence) is tuple):
        for i in sequence:
            size += for_sizeof(i,True)
    if number:
        return size + getsizeof(sequence)
    return datasize(size + getsizeof(sequence))

class datasize():
    base = {
        0 : "B",
        1 : "KiB",
        2 : "MiB",
        3 : "GiB",
        4 : "TiB",
        5 : "PiB"
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

class SHA1():
    def _block(self,step):
            return [
                i.to_bytes(self.length,self.byteorder) for i in 
                range(step,self.block_size*self.processes,self.processes)]
    def _block0(self,start):
        return [
                i.to_bytes(self.length,self.byteorder) for i in 
                range(start,self.block_size+start)
                ]
                
    def block(self,start):
        for i in range(start,self.block_size+start):
            hash = Crypto.SHA1(i.to_bytes(self.length,self.byteorder))
            if hash == self.hash:
                self.state.value = True
                self.queue.put(i.to_bytes(self.length,self.byteorder))
                
    def __init__(self,hash:bytes, processes:int, block_size=0, block_number=0):
        "2 ** block_size or blocks_number = actual value"
        block_size = 2 ** block_size
        block_number = 2 ** block_number

        self.length = 1
        self.hash = hash
        self.byteorder = "big"
        self.block_size = block_size
        self.block_number = block_number
        self.processes = processes

        modify = False
        self.queue = multiprocessing.Manager().Queue(1)
        self.state = multiprocessing.Manager().Value(ctypes.c_bool,False)
        with multiprocessing.Pool(processes) as pool:
            end = block_size*block_number
            while self.hash == hash:
                i = 0
                if modify:
                    self.block_size = block_size
                    self.block_number = block_number
                    end = block_size*block_number
                if end > 2**(self.length*8):
                    modify = True
                    while self.block_size*self.block_number > 2**(self.length*8):
                        self.block_size = int(self.block_size/2)
                        self.block_number /= 2
                    end = int(self.block_size*self.block_number)
                while i < 2**(self.length*8):
                    pool.map(self.block,range(i,i+end,self.block_size))
                    if self.state.value:
                        self.hash = self.queue.get(False)
                        break
                    i += end
                self.length += 1
            # raise Exception("Error")

    def __repr__(self) -> bytes:
        return self.hash
    def __str__(self) -> str:
        return "0x" + self.__repr__().hex()

if __name__ == "__main__":
    h = Crypto.SHA1(b"abc")
    print(SHA1(h,4,8,8))