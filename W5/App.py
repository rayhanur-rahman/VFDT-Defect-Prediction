import math, random, Num

list = [64,64,65,65,68,68,69,69,70,70,71,71,72,72,72,72,75,75,75,75,80,80,81,81,83,83,85,85]


l1 = [64,64,65,65,68,68,69,69,70,70,71,71,72,72,72,72]
l2 = [75,75,75,75,80,80,81,81,83,83,85,85]

n = Num.Num(None, None)
n2 = Num.Num(None, None)
for i in l1:
    n.increment(i)

for i in l2:
    n2.increment(i)

print(f'{n.sd} - {n2.sd} - {n.getExpectedValue(n2)} - {n2.getExpectedValue(n)}')

list.sort()
enough = math.pow(len(list), 0.5)
queue = []
queue.append(list)


while len(queue) != 0:
    poppedItem = queue.pop(0)
    low = poppedItem[0]
    high = poppedItem[len(poppedItem)-1]
    if high - low <= enough:
        print(f'{poppedItem}')
        continue
    num = Num.Num("", None)
    for item in poppedItem:
        num.increment(item)
    mean = math.ceil(num.mean)
    list1 = []
    list2 = []
    for item in poppedItem:
        if item <= mean:
            list1.append(item)
        else:
            list2.append(item)

    queue.append(list1)
    queue.append(list2)
    # print(f'{list1} and {list2}')



