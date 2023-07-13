import hashlib
import random
import time 
import sm3


def generate_collisions(num_bits, num_attempts):
    hash_dict = {}
    for _ in range(num_attempts):
        # 生成随机消息
        message = random.getrandbits(num_bits)
        
        # 计算哈希值
        hash_val = sm3(str(message).encode())
        
        # 将哈希值缩小到指定的位数
        reduced_hash = reduce_hash(int(hash_val, 16), num_bits)
        
        # 检查缩小后的哈希值是否已存在
        if reduced_hash in hash_dict:
            # 发现碰撞！
            print(f"消息 {message} 和 {hash_dict[reduced_hash]} 的哈希值发生碰撞")
            return message, hash_dict[reduced_hash]
        
        # 存储缩小后的哈希值及其对应的消息
        hash_dict[reduced_hash] = message

    # 未找到碰撞
    print("未找到碰撞.")
    return None, None


# 测试碰撞生成
num_bits = 16  # 用于缩小哈希值的位数
num_attempts = int(2**(num_bits/2)) # 尝试生成碰撞的次数
time_start=time.time() 
message1, message2 = generate_collisions(num_bits, num_attempts)
time_end=time.time() 
print('totally cost',time_end-time_start,'s')