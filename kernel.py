def SHA1(text:bytes) -> bytes:
    ROTL = lambda x,n:((x << n) | (x >> (32 - n))) & 0xffffffff

    h = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]

    byteorder = 'big'

    # 补位
    l = len(text)
    text += b'\x80' + (b'\x00' * (55 - (l % 64))) + (l * 8).to_bytes(8,byteorder)

    # 计算
    for ib in [text[i:i + 64] for i in range(0,len(text),64)]:
        # 分组
        W = []
        for i in [ib[i:i + 4] for i in range(0,len(ib),4)]:
            W.append(int.from_bytes(i,byteorder))
        for t in range(16,80):
            W.append(ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],1))
        
        # 计算
        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]

        K = 0x5a827999
        for i in range(0,20):
            T = (ROTL(a,5) + ((b & c) | ((~ b) & d)) + e + K + W[i]) & 0xffffffff
            a,b,c,d,e = T,a,ROTL(b,30),c,d

        K = 0x6ed9eba1
        for i in range(20,40):
            T = (ROTL(a,5) + (b ^ c ^ d) + e + K + W[i]) & 0xffffffff
            a,b,c,d,e = T,a,ROTL(b,30),c,d

        K = 0x8f1bbcdc
        for i in range(40,60):
            T = (ROTL(a,5) + ((b & c) ^ (b & d) ^ (c & d)) + e + K + W[i]) & 0xffffffff
            a,b,c,d,e = T,a,ROTL(b,30),c,d

        K = 0xca62c1d6
        for i in range(60,80):
            T = (ROTL(a,5) + (b ^ c ^ d) + e + K + W[i]) & 0xffffffff
            a,b,c,d,e = T,a,ROTL(b,30),c,d

        h[0] = (h[0] + a) & 0xffffffff
        h[1] = (h[1] + b) & 0xffffffff
        h[2] = (h[2] + c) & 0xffffffff
        h[3] = (h[3] + d) & 0xffffffff
        h[4] = (h[4] + e) & 0xffffffff
    
    return h[0].to_bytes(4,byteorder) + h[1].to_bytes(4,byteorder) + h[2].to_bytes(4,byteorder) + h[3].to_bytes(4,byteorder) + h[4].to_bytes(4,byteorder)
