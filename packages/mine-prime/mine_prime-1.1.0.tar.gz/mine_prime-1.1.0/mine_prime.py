import math
# 有两个函数，is_prime(n),判断n是否是素数，
#prime（n）是把n以内的所有素数放到一个列表里

def is_prime(n):
    if n<=1:
        return False
    if n==2:
        return True
    for i in range(2,int(math.sqrt(n)+1)):
        if n%i ==0:
            return False
    return True

def prime(start,stop=None):
    if stop ==None:
        stop=start
        start=2
    return [x for x in range(start,stop+1) if is_prime(x)]


