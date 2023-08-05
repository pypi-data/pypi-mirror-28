print("-------- 摇骰子下注赌游戏 --------\n")
print("游戏说明：初始本金：1000，下注后，如果赢了，获得1倍金额，输了，扣除1倍金额，本金为 0 时，游戏结束。")

import random
rollStr = ''    #系统接收下注变量
#一、系统摇点
def sysGame():
  sysNum = random.randint(1,30)
  if sysNum<11:
    rollStr = '小'
  elif sysNum>11 and sysNum<21:
    rollStr = '中'
  else:
    rollStr = '大'

  # 显示赌注信息
  print("系统下注："+ rollStr)
  return rollStr

#sysGame()

def Rolldice():
    print("\n-------- 游戏开始 --------\n")
    money = 1000  #个人金额
    userStr = ''  #下注选择  
    uMoney = 0    #下注金额  
    while money>0:
        userStr = input("请下注：小 or 中 or 大：")
        # 如果下注不输入 则默认为小
        if(userStr.strip()==''):
            userStr = '小'
            print("默认赌注为：小")
        elif userStr not in ['小','中','大']:
            print("------格式输格式有误，请重新输入------")
            userStr = input("请下注：小 or 中 or 大：")
            print("默认赌注为：小")

        inputM = input("请输入下注金额：")
        rollStr = sysGame()    
        # 如果金额不输入 则默认为100
        if(inputM.strip()==''):
            uMoney = 100
            print("默认下注金额为：100")
        else:
            uMoney = int(inputM)

        # 根据输入金额进行调整
        if(uMoney>0 and uMoney<=money):    
        #如果猜错的话进行对应调整
            if userStr!=rollStr:    
                money -= uMoney
                print("---------对不起，你猜错了---------")
                print("你现在还有 {0} 元本金".format(money))
                print("------------------------------------------------------\n")
            else:
                money += uMoney
                print("---------恭喜你猜对了---------")
                print("-恭喜，你赢了 {} 元，你现在有 {} 元本金".format(uMoney, money))
                print("------------------------------------------------------\n")
        else:
            print("---------金额超出范围或输入格式有误---------")         
    else:
        print("------------------------------------------------------")
        print("\n游戏结束\n")
        print("------------------------------------------------------")

Rolldice()   