def SHA1(data:bytes) -> bytes:
    ROTL = lambda x,n:((x << n) | (x >> (32 - n))) & 0xffffffff
    h = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]
    byteorder = 'big'

    # 补位
    l = len(data)
    data += b'\x80' + (b'\x00' * (55 - (l % 64))) + (l * 8).to_bytes(8,byteorder)
    # 计算
    for ib in [data[i:i + 64] for i in range(0,len(data),64)]:
        # 分组
        W = list()
        for i in [ib[i:i + 4] for i in range(0,len(ib),4)]:
            W.append(int.from_bytes(i,byteorder))
        for t in range(16,80):
            W.append(ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],1))
        
        # 计算
        a,b,c,d,e = h[0],h[1],h[2],h[3],h[4]

        for i in range(0,20):
            a,b,c,d,e = (ROTL(a,5) + ((b & c) | ((~ b) & d)) + e + 0x5a827999 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
        for i in range(20,40):
            a,b,c,d,e = (ROTL(a,5) + (b ^ c ^ d) + e + 0x6ed9eba1 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
        for i in range(40,60):
            a,b,c,d,e = (ROTL(a,5) + ((b & c) ^ (b & d) ^ (c & d)) + e + 0x8f1bbcdc + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
        for i in range(60,80):
            a,b,c,d,e = (ROTL(a,5) + (b ^ c ^ d) + e + 0xca62c1d6 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d

        h[0] += a
        h[1] += b
        h[2] += c
        h[3] += d
        h[4] += e
        h[0] &= 0xffffffff
        h[1] &= 0xffffffff
        h[2] &= 0xffffffff
        h[3] &= 0xffffffff
        h[4] &= 0xffffffff
    return h[0].to_bytes(4,byteorder) + h[1].to_bytes(4,byteorder) + h[2].to_bytes(4,byteorder) + h[3].to_bytes(4,byteorder) + h[4].to_bytes(4,byteorder)

class SHA1s:
    def __calculate(self,data:bytes,h:bytes) -> bytes:
        ROTL = lambda x,n:((x << n) | (x >> (32 - n))) & 0xffffffff
        byteorder = 'big'
        for ib in [data[i:i + 64] for i in range(0,len(data),64)]:
            # 分组
            W = list()
            for i in [ib[i:i + 4] for i in range(0,len(ib),4)]:
                W.append(int.from_bytes(i,byteorder))
            for t in range(16,80):
                W.append(ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],1))
            
            # 计算
            a,b,c,d,e = h[0],h[1],h[2],h[3],h[4]

            for i in range(0,20):
                a,b,c,d,e = (ROTL(a,5) + ((b & c) | ((~ b) & d)) + e + 0x5a827999 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
            for i in range(20,40):
                a,b,c,d,e = (ROTL(a,5) + (b ^ c ^ d) + e + 0x6ed9eba1 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
            for i in range(40,60):
                a,b,c,d,e = (ROTL(a,5) + ((b & c) ^ (b & d) ^ (c & d)) + e + 0x8f1bbcdc + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
            for i in range(60,80):
                a,b,c,d,e = (ROTL(a,5) + (b ^ c ^ d) + e + 0xca62c1d6 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d

            h[0] += a
            h[1] += b
            h[2] += c
            h[3] += d
            h[4] += e
            h[0] &= 0xffffffff
            h[1] &= 0xffffffff
            h[2] &= 0xffffffff
            h[3] &= 0xffffffff
            h[4] &= 0xffffffff
        return h

    def __init__(self,data:bytes=b'') -> None:
        self.__h = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]
        self.length = len(data)
        if self.length > 64:
            self.__h = self.__calculate(data[:(self.length - self.length % 64)],self.__h)
            self.__data = data[(self.length - self.length % 64):]
            self.__surplus = self.length % 64
        else:
            self.__data = data
            self.__surplus = self.length
    def append(self,data:bytes) -> None:
        self.__data += data
        length = len(data)
        self.__surplus += length
        self.length += length
        if self.__surplus > 64:
            self.__h = self.__calculate(self.__data[:(self.__surplus - self.__surplus % 64)],self.__h)
            self.__data = data[(self.__surplus - self.__surplus % 64):]
            self.__surplus = self.__surplus % 64
    def get(self) -> bytes:
        byteorder = 'big'
        self.__data += b'\x80' + (b'\x00' * (55 - self.__surplus % 64)) + (self.length * 8).to_bytes(8,byteorder)
        h = self.__calculate(self.__data,self.__h)
        return h[0].to_bytes(4,byteorder) + h[1].to_bytes(4,byteorder) + h[2].to_bytes(4,byteorder) + h[3].to_bytes(4,byteorder) + h[4].to_bytes(4,byteorder)
