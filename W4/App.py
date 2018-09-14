import Config, Sample, math, random, Num, Sym

random.seed(0)

cfg = Config.Config()

print("\n---Sample---")
streamOfRandomNumbers = cfg.GenerateStreamOfRandomNumbers()

samples = []

for i in range(4,11):
    s = Sample.Sample(math.pow(2,i))
    samples.append(s)

for item in samples:
    for number in streamOfRandomNumbers:
        item.increment(number)
    item.sort()
    print(str(item.getPercentile(50)))


print("\n---Num---")

samples = [4,10,15,38,54,57,62,83,100,100,174,190,215,225,233,250,260,270,299,300,306,333,350,375,443,475,525,583,780,1000]
num1 = Num.Num("")

for item in samples:
    num1.increment(item)

print(num1.sd)
print(num1.variance)

print("\n---Sym---")
symbols = ['y','y','y','y','y','y','y','y','y','n','n','n','n','n']
sym1 = Sym.Sym("")

for item in symbols:
    sym1.increment(item)
print(sym1.getEntropy())
