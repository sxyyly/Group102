

import struct
import numpy as np
import numba as nb
import threading


def sm3(message):
    padded_message = padding(message)
    blocks = divide_blocks(padded_message)
    hash_value = np.array([0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e], dtype=np.uint32)
    
    for block in blocks:
        hash_value = compress(hash_value, block)
    
    return ''.join(format(h, '08x') for h in hash_value)



def padding(message):
    message_length = len(message)
    padding_length = (56 - (message_length + 1) % 64) % 64  # 计算填充长度
    message = message.encode('utf-8')  # 将 message 转换为字节对象
    message += b"\x80" + b"\x00" * padding_length  # 添加填充位和填充字节

    message_length_bytes = (message_length * 8).to_bytes(8, 'big')  # 消息长度以大端字节序表示
    message += message_length_bytes
    
    return message




def divide_blocks(message):
    num_blocks = len(message) * 8 // 512
    blocks = np.frombuffer(message, dtype=np.uint32).reshape(num_blocks, 16).copy()
    return blocks


@nb.njit(parallel=True)
def compress(hash_value, blocks):
    T = np.array([0x79cc4519, 0x7a879d8a], dtype=np.uint32)
    
    for block in nb.prange(blocks.shape[0]):
        w = expand(blocks[block])
        v = hash_value.copy()
        
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
        
        for i in range(8):
            hash_value[i] ^= v[i]
    
    return hash_value


def expand(block):
    w = np.zeros(64, dtype=np.uint32)
    
    for i in range(16):
        w[i] = block[i]
    
    for i in range(16, 64):
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


secret="Hello World"
print(sm3(secret))
