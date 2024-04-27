

# 例子1：寻找三位数的水仙花数。
from random import randint
for num in range(100, 1000):       # 左闭右开
    low = num % 10
    mid = (num//10) % 10
    high = num//100
    if num == low**3 + mid**3 + high**3:
        print(num)


# 例子2：正整数的反转
num = int(input('num = '))
reversed_num = 0
while num > 0:
    reversed_num = reversed_num*10 + num % 10
    num = num//10
print(reversed_num)


# 例子3：百钱白鸡问题
for x in range(0, 20):
    for y in range(0, 33):
        z = 100 - x - y
        if 5 * x + 3 * y + z / 3 == 100:
            print('公鸡:', x, '只, 母鸡:', y, '只, 小鸡:', z, '只')


# 例子4：CRAPS赌博游戏

money = 1000
while money > 0:                          # 只要money > 0, 游戏就继续
    print(f'你的总资产为: {money}元')
    go_on = False
    # 下注金额必须大于0小于等于玩家总资产
    while True:                           # 建了一个无限循环，意味着循环会一直执行下去，直到出现 break 或程序终止的情况。
        debt = int(input('请下注: '))
        if 0 < debt <= money:             # 检查下注金额是否合法
            break                         # break 语句是与内部的 if 条件语句相连的，如果合法，则跳出内部的 while 循环
    # 第一次摇色子
    # 用1到6均匀分布的随机数模拟摇色子得到的点数
    first = randint(1, 6) + randint(1, 6)
    print(f'\n玩家摇出了{first}点')
    if first == 7 or first == 11:
        print('玩家胜!\n')
        money += debt
    elif first == 2 or first == 3 or first == 12:     # elif（即"else if"的缩写）用来检查另一个条件，如果第一个if的条件不成立时才会评估。
        print('庄家胜!\n')
        money -= debt
    else:                                  # 如果前面的if和elif条件都不满足，则执行else
        go_on = True                       # 返回到最前面的go_on，因为是True，所以游戏继续
    # 第一次摇色子没有分出胜负游戏继续
    while go_on:
        go_on = False
        current = randint(1, 6) + randint(1, 6)
        print(f'玩家摇出了{current}点')
        if current == 7:
            print('庄家胜!\n')
            money -= debt
        elif current == first:
            print('玩家胜!\n')
            money += debt
        else:
            go_on = True
print('你破产了, 游戏结束!')




import os

print(os.cpu_count())
