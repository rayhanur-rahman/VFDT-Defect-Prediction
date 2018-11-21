import Utils, math, random, timeit, numpy as np

def getBins(list):
    ls = []
    for item in list:
        ls.append(item['a'])
    hist, bin_edges = np.histogram(ls, bins=int(math.sqrt(len(ls))))


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


def de(fobj, bounds, mut=0.8, crossp=0.7, popsize=20, its=1000):
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]


def testFunc(args):
    return args[0]*args[1]

it = list(de(testFunc, bounds=[(5, 25), (-10,10)]))
print(it[-1])