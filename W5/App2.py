import math, random

import sys
sys.path.insert(0, '../W4/')

import Num

list = [64,64,65,65,68,68,69,69,70,70,71,71,72,72,72,72,75,75,75,75,80,80,81,81,83,83,85,85]
list.sort()
enough = math.pow(len(list), 0.5)
queue = []
queue.append(list)

# n = Num.Num("", "")
#
# for x in list:
#     n.increment(x)
#     print(f'{n.mean: .2f} {n.variance: .2f} {n.sd: .2f}')
#
# print(100*'#')
#
# # list.sort(reverse=True)
#
# for x in list:
#     n.decrement(x)
#     print(f'{n.mean: .2f} {n.variance: .2f} {n.sd: .2f}')

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
    for item in poppedItem:
        num1.decrement(item)
        num2.increment(item)
        if num1.count >= enough and num2.count >= enough:
            expectedValueOfSd = num1.getExpectedValue(num2)
            if expectedValueOfSd < best:
                cut = item
    list1 = []
    list2 = []
    for item in poppedItem:
        if item <= cut:
            list1.append(item)
        else:
            list2.append(item)

    queue.append(list1)
    queue.append(list2)
    # print(f'{list1} and {list2}')




