# import random
# point=random.randint(1,7)#1-6取随机值，摇骰子。
# print(point)
import random


def roll_dice(numbers=3, points=None):    #先摇三个骰子
    print("==========摇骰子==========")
    if points is None:          #定义一个列表
        points = []
    while numbers > 0:
        point = random.randrange(1, 7)          #向列表中随机三个数 当三个骰子
        points.append(point)
        numbers = numbers - 1
    return points               #随机的骰子结果


def roll_result(total):
    isBig = 11 <= total <= 18       #11-18为大
    isSmall = 3 <= total <= 10      #3-10为小
    if isBig:
        return '大'
    elif isSmall:
        return '小'


def start_game():
    your_money = 1000
    while your_money > 0:               #有钱的时候开始游戏，钱<0游戏结束。
        print("==========游戏开始==========")
        choices = ['大', '小']
        your_choice = input('请下注，大 or 小：')
        your_bet = input('下注金额：')
        if your_choice in choices:   #只有输入值为“大”或“小”游戏才能正常进行，否则报错。
            points = roll_dice()        #获取骰子随机的点数结果
            total = sum(points)        # sum() 计算每次随机后三个数的总和 
            youWin = your_choice == roll_result(total)          #调用函数roll_result(total)
            if youWin:      #赢的时候
                print('骰子点数：', points)  #调用函数roll_dice()
                print('恭喜，你赢了 {} 元，你现在有 {} 元本金'.format(
                    your_bet, your_money + int(your_bet)))      #原有金额加上下注金额等于最后金额
                your_money = your_money + int(your_bet)
            else:       #输的时候
                print('骰子点数：', points)
                print('很遗憾，你输了 {} 元，你现在有 {} 元本金'.format(
                    your_bet, your_money - int(your_bet)))
                your_money = your_money - int(your_bet)
        else:
            print('格式有误，请重新输入')
    else:
        print('游戏结束')

# start_game()    #游戏开始
