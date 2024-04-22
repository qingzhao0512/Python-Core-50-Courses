

# 例子1：寻找三位数的水仙花数。
for num in range(100, 1000):       # 左闭右开
    low = num % 10
    mid = (num//10) % 10
    high = num//100
    if num == low**3 + mid**3 + high**3:
        print(num)
