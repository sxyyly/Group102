import hashlib
import random
import time 


def sm3(message):
    # 填充消息
    padded_message = padding(message)
    
    # 分块处理
    blocks = divide_blocks(padded_message)
    
    # 初始化哈希值
    hash_value = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
    
    # 压缩函数迭代
    for block in blocks:
        hash_value = compress(hash_value, block)
    
    # 输出哈希值
    return ''.join(format(h, '08x') for h in hash_value)

def padding(message):
    # 消息长度（以比特为单位）
    message_length = len(message) * 8
    
    # 填充比特
    padding_bits = "10000000"
    
    # 计算填充的字节数
    padding_length = (56 - (message_length + 1) % 512 // 8) % 64
    
    # 填充消息
    padded_message = message + bytes.fromhex(padding_bits) + b'\x00' * padding_length + message_length.to_bytes(8, 'big')
    
    return padded_message

def divide_blocks(message):
    # 将消息分块（每块512比特）
    blocks = []
    num_blocks = len(message) * 8 // 512
    
    for i in range(num_blocks):
        block = message[i * 64 : (i + 1) * 64]
        blocks.append(block)
    
    return blocks

def compress(hash_value, block):
    # 定义置换常量
    T = [0x79cc4519, 0x7a879d8a]
    
    # 消息扩展
    w = expand(block)
    
    # 消息分组
    v = hash_value[:]
    
    # 压缩函数迭代
    for i in range(64):
        if i < 16:
            ss1 = (rotate_left(v[0], 12) + v[4] + rotate_left(T[0], i)) & 0xFFFFFFFF
        else:
            ss1 = (rotate_left(v[0], 12) + v[4] + rotate_left(T[1], i)) & 0xFFFFFFFF
        ss1 = rotate_left(ss1, 7) & 0xFFFFFFFF
        ss2 = ss1 ^ rotate_left(v[0], 12) & 0xFFFFFFFF
        tt1 = (ff(v[0], v[1], v[2], i) + v[3] + ss2 + w[i]) & 0xFFFFFFFF
        tt2 = (gg(v[4], v[5], v[6], i) + v[7] + ss1 + w[i]) & 0xFFFFFFFF
        v[3] = v[2]
        v[2] = rotate_left(v[1], 9) & 0xFFFFFFFF
        v[1] = v[0]
        v[0] = tt1
        v[7] = v[6]
        v[6] = rotate_left(v[5], 19) & 0xFFFFFFFF
        v[5] = v[4]
        v[4] = p0(tt2)
    
    # 更新哈希值
    for i in range(8):
        hash_value[i] ^= v[i]
    
    return hash_value

def expand(block):
    # 将消息块扩展为消息扩展
    w = [0] * 64
    
    for i in range(16):
        w[i] = int.from_bytes(block[i * 4 : (i + 1) * 4], 'big')
    
    for i in range(16, 64):
        w[i] = p1(w[i - 16] ^ w[i - 9] ^ rotate_left(w[i - 3], 15)) ^ rotate_left(w[i - 13], 7) ^ w[i - 6]
    
    return w

def rotate_left(x, n):
    # 循环左移
    n = n % 32  # 对移位数取模，确保在 0 到 31 的范围内
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def ff(x, y, z, i):
    # 置换函数FF
    if 0 <= i < 16:
        return x ^ y ^ z
    elif 16 <= i < 64:
        return (x & y) | (x & z) | (y & z)

def gg(x, y, z, i):
    # 置换函数GG
    if 0 <= i < 16:
        return x ^ y ^ z
    elif 16 <= i < 64:
        return (x & y) | (~x & z)

def p0(x):
    # 置换函数P0
    return x ^ rotate_left(x, 9) ^ rotate_left(x, 17)

def p1(x):
    # 置换函数P1
    return x ^ rotate_left(x, 15) ^ rotate_left(x, 23)

def reduce_hash(hash_val, num_bits):
    # 将哈希值缩小到指定的位数
    mask = (1 << num_bits) - 1
    return hash_val & mask
