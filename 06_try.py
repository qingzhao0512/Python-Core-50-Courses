

num = int(input('请输入一个正整数: '))
# 双星号（**）是幂运算符,计算 num 的平方根，并将结果转换为整数，存储在变量 end 中。这样做的目的是减少后面循环的迭代次数，因为一个数的因子不可能超过它的平方根
end = int(num ** 0.5)
is_prime = True                 # 假设 num 是素数
for x in range(2, end + 1):
    if num % x == 0:
        is_prime = False
        break
if is_prime and num != 1:          # 如果循环结束后，is_prime 仍然为 True，并且 num 不是1（因为1不是素数），则打印出 num 是素数的提示
    print(f'{num}是素数')
else:
    print(f'{num}不是素数')


# 输入两个正整数计算它们的最大公约数和最小公倍数
x = int(input('x = '))
y = int(input('y = '))
for factor in range(x, 0, -1):                # 从 x 开始往 0 递减
    # 在每次循环中，检查当前的因子 factor 是否同时能整除 x 和 y。如果能，说明 factor 是 x 和 y 的一个公约数。
    if x % factor == 0 and y % factor == 0:
        print(f'{x}和{y}的最大公约数是{factor}')
        print(f'{x}和{y}的最小公倍数是{x * y // factor}')
        break
