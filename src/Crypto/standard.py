def SHA1(M:bytes) -> bytes:
    """
    Secure Hash Standard (SHS) (NIST.FIPS.180-4 (2015-08-04))
    https://www.nist.gov/publications/secure-hash-standard
    https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
    """
    # 初始化变量
    # 数据长度
    e = len(M) * 8
    ROTL = lambda x,n,w=32:((x << n) | (x >> (w - n))) % 2**w
    
    # Functions And Constants 函数和常量 (NIST.FIPS.180-4 第4节)
    # SHA-1 Functions 函数 (NIST.FIPS.180-4 第4.1.1节)
    def f(t, x, y, z):
        Ch = lambda x,y,z: (x&y) ^ ((~x)&z)
        Parity = lambda x,y,z: x ^ y ^ z
        Maj = lambda x,y,z: (x&y) ^ (x&z) ^ (y&z)
        if 0 <= t <= 19: return Ch(x,y,z)
        elif 20 <= t <= 39: return Parity(x,y,z)
        elif 40 <= t <= 59: return Maj(x,y,z)
        elif 60 <= t <= 79: return Parity(x,y,z)
    # SHA-1 Constants 常量 (NIST.FIPS.180-4 第4.2.1节)
    def K(t):
        if 0 <= t <= 19: return 0x5a827999
        elif 20 <= t <= 39: return 0x6ed9eba1
        elif 40 <= t <= 59: return 0x8f1bbcdc
        elif 60 <= t <= 79: return 0xca62c1d6
    
    # SHA-1 Preprocessing 预处理 (NIST.FIPS.180-4 第6.1.1节):
    # Padding the Message 填充消息 (NIST.FIPS.180-4 第5.1.1节): 
    # 附加 0b10000000 到 M 末尾 
    M += b"\x80"
    # 附加 k/8 个 0b00000000, k 是 e+1+k=448mod512 的最小非负解 (NIST.FIPS.180-4 第5.1.1节)
    M += b"\x00" * ((448-((e+8)%512)) // 8)
    # 附加 64bit 的数据长度(以bit为单位, 大端序big-endian)
    M += e.to_bytes(8, "big")
    # Parsing the Message 分解消息 (NIST.FIPS.180-4 第5.2.1节): 
    # M = [[M[i0:i0+64][i1:i1+4] for i1 in range(0,64,4)] for i0 in range(0,(e//512+1)*64,64)]
    # 将 M 分解成 N 个 512bit
    N = ((e+32)//512+1)
    M = [M[i:i+64] for i in range(0,N*64,64)]
    # 将每个 512bit 分解成 16 个 32bit 
    M = [[int.from_bytes(Mi[i:i+4],"big") for i in range(0,64,4)] for Mi in M]
    # Setting the Initial Hash Value 设置初始Hash值 (NIST.FIPS.180-4 第5.3.1节): 
    H = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]
    
    # SHA-1 Hash Computation 哈希计算 (NIST.FIPS.180-4 第6.1.2节):
    for i in range(N):
        W = [None] * 80
        W[0:16] = M[i]
        t = 16
        for t in range(16,80):
            W[t] = ROTL(W[t-3]^W[t-8]^W[t-14]^W[t-16],1)
        
        a,b,c,d,e = H
        
        for t in range(80):
            T = (ROTL(a,5) + f(t,b,c,d) + e + K(t) + W[t]) % 2**32
            e = d
            d = c
            c = ROTL(b,30)
            b = a
            a = T

        H[0] = (a+H[0]) % 2**32
        H[1] = (b+H[1]) % 2**32
        H[2] = (c+H[2]) % 2**32
        H[3] = (d+H[3]) % 2**32
        H[4] = (e+H[4]) % 2**32
    Hash = H[0].to_bytes(4,"big")
    Hash += H[1].to_bytes(4,"big")
    Hash += H[2].to_bytes(4,"big")
    Hash += H[3].to_bytes(4,"big")
    Hash += H[4].to_bytes(4,"big")
    return Hash

    