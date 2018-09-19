import math, random

import Num, Sym

list = [64,64,65,65,68,68,69,69,70,70,71,71,72,72,72,72,75,75,75,75,80,80,81,81,83,83,85,85]
list = [193,215,200,210,208,150,180,180,160,198,225,167,180,170,175,165,155,190,130,140,175,145,150,158,215,175,170,150,129,150,145,130,150,220,215,225,160,225,165,175,153,150,175,153,150,150]
list = [1,2,22,22,22,23]
list.sort()
enough = math.pow(len(list), 0.5)
queue = []
queue.append(list)


while len(queue) != 0:
    poppedItem = queue.pop(0)
    low = 0
    high = len(poppedItem)
    if high - low < 2*enough:
        print(f'{poppedItem}')
        continue
    num1 = Num.Num("", None)
    num2 = Num.Num("", None)
    for item in poppedItem:
        num1.increment(item)
    best = num1.sd
    cut = None
    for index in range(0, len(poppedItem)):
        num1.decrement(poppedItem[index])
        num2.increment(poppedItem[index])
        if num1.count >= enough and num2.count >= enough:
            expectedValueOfSd = num1.getExpectedValue(num2)
            if expectedValueOfSd < best*1.05:
                cut = index
                break
    list1 = []
    list2 = []
    for index in range(0, len(poppedItem)):
        if index < cut:
            list1.append(poppedItem[index])
        else:
            list2.append(poppedItem[index])

    queue.append(list1)
    queue.append(list2)




