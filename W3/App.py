import sys

sys.path.insert(0, '../W1/')
import Config, Sample, math, random, Num, Sym, TestRig

random.seed(0)

streamOfRandomNumbers = Config.Config.GenerateStreamOfRandomNumbers()
num = Num.Num(None, None)
sym = Sym.Sym(None, None)
samples = []


def testSample():
    for i in range(4, 11):
        s = Sample.Sample(math.pow(2, i))
        samples.append(s)

    print("Size:\t50th Percentile")

    for item in samples:
        for number in streamOfRandomNumbers:
            item.increment(number)
        item.sort()
        print(f'{item.maximumSize:0000.0f} :\t {item.getPercentile(50):.2f}')
        assert True == Config.Config.Close(item.getPercentile(50), 0.5, 0.33)


TestRig.O.k(testSample)

samples = [4, 10, 15, 38, 54, 57, 62, 83, 100, 100, 174, 190, 215, 225, 233, 250, 260, 270, 299, 300, 306, 333, 350,
           375, 443, 475, 525, 583, 780, 1000]


def testNum():
    for item in samples:
        num.increment(item)
    print(f"mean & sd")
    print(f"{num.mean:0.2f} & {num.sd:0.2f}")
    assert num.mean == 270.3 and Config.Config.Close(num.sd, 231.946, 0.33) == True


TestRig.O.k(testNum)

symbols = ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'n', 'n', 'n', 'n']


def testSym():
    for item in symbols:
        sym.increment(item)
    print("Entropy")
    print(sym.getEntropy())
    assert Config.Config.Close(sym.getEntropy(), .9403, .01)


TestRig.O.k(testSym)
