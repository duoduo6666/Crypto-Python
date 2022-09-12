def SHA1(data:bytes) -> bytes:
    ROTL,byteorder,h,l = lambda x,n:((x << n) | (x >> (32 - n))) & 0xffffffff,'big',[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0],len(data)
    
    # 补位
    data += b'\x80' + (b'\x00' * (55 - (l % 64))) + (l * 8).to_bytes(8,byteorder)
    # 计算
    for ib in (data[i:i + 64] for i in range(0,len(data),64)):
        # 分组
        W = [0] * 0x50
        W[0:16] = [int.from_bytes(ib[i:i + 4],byteorder) for i in range(0,64,4)]
        for t in range(16,80): W[t] |= ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],1)
        
        # 计算
        a,b,c,d,e = h[0],h[1],h[2],h[3],h[4]

        for i in range(0,20): a,b,c,d,e = (ROTL(a,5) + ((b & c) | ((~ b) & d)) + e + 0x5a827999 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
        for i in range(20,40): a,b,c,d,e = (ROTL(a,5) + (b ^ c ^ d) + e + 0x6ed9eba1 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
        for i in range(40,60): a,b,c,d,e = (ROTL(a,5) + ((b & c) ^ (b & d) ^ (c & d)) + e + 0x8f1bbcdc + W[i]) & 0xffffffff,a,ROTL(b,30),c,d
        for i in range(60,80): a,b,c,d,e = (ROTL(a,5) + (b ^ c ^ d) + e + 0xca62c1d6 + W[i]) & 0xffffffff,a,ROTL(b,30),c,d

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
    __slots__ = ('_h','_data','_surplus','_ROTL','_byteorder','length')
    def __calculate(self,data:bytes,h:bytes) -> bytes:
        for ib in (data[i:i + 64] for i in range(0,len(data),64)):
            # 分组
            W = [0] * 0x50
            W[0:16] = [int.from_bytes(ib[i:i + 4],self._byteorder) for i in range(0,64,4)]
            for t in range(16,80): W[t] |= self._ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],1)
            
            # 计算
            a,b,c,d,e = h[0],h[1],h[2],h[3],h[4]

            for i in range(0,20): a,b,c,d,e = (self._ROTL(a,5) + ((b & c) | ((~ b) & d)) + e + 0x5a827999 + W[i]) & 0xffffffff,a,self._ROTL(b,30),c,d
            for i in range(20,40): a,b,c,d,e = (self._ROTL(a,5) + (b ^ c ^ d) + e + 0x6ed9eba1 + W[i]) & 0xffffffff,a,self._ROTL(b,30),c,d
            for i in range(40,60): a,b,c,d,e = (self._ROTL(a,5) + ((b & c) ^ (b & d) ^ (c & d)) + e + 0x8f1bbcdc + W[i]) & 0xffffffff,a,self._ROTL(b,30),c,d
            for i in range(60,80): a,b,c,d,e = (self._ROTL(a,5) + (b ^ c ^ d) + e + 0xca62c1d6 + W[i]) & 0xffffffff,a,self._ROTL(b,30),c,d

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
        self._h,self._ROTL,self.length,self._byteorder = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0],lambda x,n:((x << n) | (x >> (32 - n))) & 0xffffffff,len(data),'big'
        if self.length > 64:
            self._h,self._data,self._surplus = self.__calculate(data[:(self.length - self.length % 64)],self._h),data[(self.length - self.length % 64):],self.length % 64
        else:
            self._data, self._surplus = data, self.length
    def append(self,data:bytes) -> None:
        self._data += data
        length = len(data)
        self._surplus += length
        self.length += length
        if self._surplus > 64:
            self._h,self._data = self.__calculate(self._data[:(self._surplus - self._surplus % 64)],self._h),data[(self._surplus - self._surplus % 64):]
            self._surplus %= 64
    def get(self) -> bytes:
        h = self.__calculate(self._data+(b'\x80' + (b'\x00' * (55 - self._surplus % 64)) + (self.length * 8).to_bytes(8,self._byteorder)),self._h)
        return h[0].to_bytes(4,self._byteorder) + h[1].to_bytes(4,self._byteorder) + h[2].to_bytes(4,self._byteorder) + h[3].to_bytes(4,self._byteorder) + h[4].to_bytes(4,self._byteorder)

def Base64_encode(data:bytes,padding:str='=',table:dict[int:str]=
    {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',
    13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',
    26:'a',27:'b',28:'c',29:'d',30:'e',31:'f',32:'g',33:'h',34:'i',35:'j',36:'k',37:'l',38:'m',
    39:'n',40:'o',41:'p',42:'q',43:'r',44:'s',45:'t',46:'u',47:'v',48:'w',49:'x',50:'y',51:'z',
    52:'0',53:'1',54:'2',55:'3',56:'4',57:'5',58:'6',59:'7',60:'8',61:'9',62:'+',63:'/'}
    ) -> str:
    b,Base64 = ((len(data) % 3) ^ 3) % 3,''
    data += b'\x00' * b
    for i in (data[i:i + 3] for i in range(0,len(data),3)):
        Base64 += table[i[0] >> 2]
        Base64 += table[((i[0] << 4) & 0x30) | (i[1] >> 4) & 0x0f]
        Base64 += table[((i[1] << 2) & 0x3c) | (i[2] >> 6) & 0x03]
        Base64 += table[i[2] & 0x3f]
    if not b: return Base64
    return Base64[:-b] + (padding * b)

def Base64_decode(Base64:str,padding:str='=',table:dict[str:int]=
    {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,
    'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,
    'a':26,'b':27,'c':28,'d':29,'e':30,'f':31,'g':32,'h':33,'i':34,'j':35,'k':36,'l':37,'m':38,
    'n':39,'o':40,'p':41,'q':42,'r':43,'s':44,'t':45,'u':46,'v':47,'w':48,'x':49,'y':50,'z':51,
    '0':52,'1':53,'2':54,'3':55,'4':56,'5':57,'6':58,'7':59,'8':60,'9':61,'+':62,'/':63}
    ) -> bytes:
    data,table[padding] = b'',255
    for i in (Base64[i:i + 4] for i in range(0,len(Base64),4)):
        b = [0,0,0]
        b[0] = table[i[0]] << 2 | table[i[1]] >> 4
        b[1] = (table[i[1]] << 4 & 0xf0) | (table[i[2]] >> 2 & 0x0f)
        b[2] = (table[i[2]] << 6 & 0xc0) | table[i[3]]
        data += bytes(b)
    if Base64[-1] == padding: 
        if Base64[-2] == padding:
            return data[:-2]
        return data[:-1]
    return data
    
