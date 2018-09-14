import csv,sys, Num, Sym

nums = []
syms = []


with open('auto.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 1
    toBeIgnored = []
    toBeParsedToInt = []
    titles = []
    for row in csv_reader:
        for index in range(0, len(row)):
            item = row[index].strip()
            titles.append(item)
            if line_count == 1:
                if '?' in item:
                    toBeIgnored.append(index)
                if '$' in item:
                    toBeParsedToInt.append(index)
                if '>' in item:
                    toBeParsedToInt.append(index)
                if '<' in item:
                    toBeParsedToInt.append(index)
            if index not in toBeIgnored:
                if line_count == 1:
                    if index not in toBeParsedToInt:
                        syms.append(Sym.Sym(item))
                    if index in toBeParsedToInt:
                        nums.append(Num.Num(item))
                else:
                    if index not in toBeParsedToInt:
                        sym = next((x for x in syms if x.title == titles[index]), None)
                        sym.increment(item)
                    if index in toBeParsedToInt:
                        num = next((x for x in nums if x.title == titles[index]), None)
                        if '?' not in item:
                            num.increment(float(item))

        line_count += 1

for item in syms:
    print(item.title, end=" ")
    print(item.total, end=" ")
    print(item.mode, end=" ")
    print(item.most, end=" ")
    print(item.frequency)
    print(item.getEntropy())
    print("*********")



for item in nums:
    print(item.title, end=" ")
    print(item.count, end=" ")
    print(item.mean, end=" ")
    print(item.variance, end=" ")
    print(item.sd, end=" ")
    print(item.min, end=" ")
    print(item.max, end=" ")
    print("\n***\n")

