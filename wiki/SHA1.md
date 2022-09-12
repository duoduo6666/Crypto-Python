# SHA1 函数

## 描述
计算一组数据的 SHA-1 值

### 语法
`Crypto.SHA1(data)`

### 参数
|参数|描述|
|----|----|
|data|数据|

### 返回值
返回 data 参数的SHA-1值

### 实例
打印 'abc' 的SHA-1值
```Python
print(hex(int.from_bytes(Crypto.SHA1(b'abc'))))
```