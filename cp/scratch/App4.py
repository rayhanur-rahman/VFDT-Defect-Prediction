import Utils, math, random, timeit, numpy

def getBins(list):
    ls = []
    for item in list:
        ls.append(item['a'])
    hist, bin_edges = numpy.histogram(ls, bins=int(math.sqrt(len(ls))))


def getDiscretizedRangeNumPy(data, attribute):
    length = len(data)
    if length == 0: return None, None, None
    list = []
    for item in data:
        list.append(item[attribute])
    enough = math.pow(len(list), 0.5)
    hist, bin_edges = numpy.histogram(list, bins=int( 3 ))

    minRange = []
    maxRange = []
    cuts = []

    for index in range(0, len(bin_edges)):
        cuts.append(int(bin_edges[index]))
        if index != len(bin_edges) - 1: minRange.append(int(bin_edges[index]))
        if index != 0: maxRange.append(int(bin_edges[index]))

    cuts = cuts[1:-1]
    return minRange, maxRange, cuts



random.seed(0)

list = []
list2 = []

for x in range(0, 1000):
    r = random.randint(0, 1000)
    list.append({'a' : r})
    list2.append(r)

start = timeit.default_timer()

list.sort(key=lambda k : k['a'])
print(f'{list[0]} {list[-1]}')

x = Utils.getDiscretizedRange(list, 'a')
end = timeit.default_timer()
print(f'{end - start}')
print(x)

start = timeit.default_timer()
print(getDiscretizedRangeNumPy(list, 'a'))
end = timeit.default_timer()
print(f'{end - start}')


