import math, random, Num, Sym, Rows, csv, Model, typing
from operator import attrgetter
from typing import List


def csvRowsGenerator():
    with open("weatherLong.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            yield row


line_count = 1
listOfWeatherData = []


for row in csvRowsGenerator():
    if line_count > 1:
        outlook = row[0].strip().replace('\n','')
        temp = float(row[1].strip().replace('\n',''))
        humid = float(row[2].strip().replace('\n',''))
        wind = row[3].strip().replace('\n','')
        play = row[4].strip().replace('\n','')
        weather = Model.Weather(outlook, float(temp), float(humid), wind, play)
        listOfWeatherData.append(weather)
    line_count += 1


listOfWeatherData.sort(key=lambda x: x.temp)

enough = math.pow(len(listOfWeatherData), 0.5)
queue = []
queue.append(listOfWeatherData)

finalQueue = []

while len(queue) != 0:
    poppedItem = queue.pop(0)
    low = 0
    high = len(poppedItem)
    min = 123456789
    max = -123456789;
    if high - low < 2*enough:
        for element in poppedItem:
            if min > element.temp:
                min = element.temp
            if max < element.temp:
                max = element.temp
            # print(element.temp, end=" ")
        # print("")
        for element in poppedItem:
            element.tempRangeMax = max
            element.tempRangeMin = min
        finalQueue.append(poppedItem)
        continue
    num1 = Num.Num("", None)
    num2 = Num.Num("", None)
    for item in poppedItem:
        num1.increment(item.temp)
    best = num1.sd
    cut = None
    for item in poppedItem:
        num1.decrement(item.temp)
        num2.increment(item.temp)
        if num1.count >= enough and num2.count >= enough:
            expectedValueOfSd = num1.getExpectedValue(num2)
            if expectedValueOfSd < best:
                cut = item.temp
    list1 = []
    list2 = []
    for item in poppedItem:
        if item.temp <= cut:
            list1.append(item)
        else:
            list2.append(item)

    queue.append(list1)
    queue.append(list2)

listOfProcessedWeatherObjects = []

for element in finalQueue:
    for item in element:
        listOfProcessedWeatherObjects.append(item)

listOfProcessedWeatherObjects.sort(key=lambda x: x.tempRangeMin)

for item in listOfProcessedWeatherObjects:
    print(f'{item.outlook} {item.temp:.0f} {item.humid:.0f} {item.wind} {item.play} {item.tempRangeMin:.0f}..{item.tempRangeMax:.0f} ')