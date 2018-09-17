import csv,sys, Num, Sym

class Table:

    def __init__(self, csvfile):
        self.nums = []
        self.syms = []
        self.isClass = {}
        self.goals = {}
        self.status = {}

        with open(csvfile) as csv_file:
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
                            self.goals[item] = 'max'
                            self.status[item] = "dependent"
                        if '<' in item:
                            toBeParsedToInt.append(index)
                            self.goals[item] = 'min'
                            self.status[item] = "independent"
                        if '!' in item:
                            self.isClass[item] = True
                        if '%' in item:
                            pass
                    if index not in toBeIgnored:
                        if line_count == 1:
                            if index not in toBeParsedToInt:
                                self.syms.append(Sym.Sym(item, index))
                            if index in toBeParsedToInt:
                                self.nums.append(Num.Num(item, index))
                        else:
                            if index not in toBeParsedToInt:
                                sym = next((x for x in self.syms if x.title == titles[index]), None)
                                if '?' not in item:
                                    sym.increment(item)
                            if index in toBeParsedToInt:
                                num = next((x for x in self.nums if x.title == titles[index]), None)
                                if '?' not in item:
                                    num.increment(float(item))

                line_count += 1
        self.setMeta()
        self.showStatistics()

    def showStatistics(self):
        print("(Id, title, total, mode, frequency)")
        for item in self.syms:
            print(f'({item.columnIndex}, {item.title}, {item.total}, {item.mode}, {item.most})')

        print("")

        print("(Id, title, total, mean, standard deviation)")
        for item in self.nums:
            print(f'({item.columnIndex}, {item.title}, {item.count}, {item.mean : 0.2f}, {item.sd : 0.2f})')
        print('---###---\n')

    def setMeta(self):
        for key in self.goals:
            # print(f'{key} -> {self.goals[key]}')
            num = next((x for x in self.nums if x.title == key), None)
            if num is not None: num.goal = self.goals[key]
        for key in self.isClass:
            # print(f'{key} -> {self.isClass[key]}')
            sym = next((x for x in self.syms if x.title == key), None)
            if sym is not None: sym.isClass = self.isClass[key]
        for key in self.status:
            # print(f'{key} -> {self.status[key]}')
            num = next((x for x in self.nums if x.title == key), None)
            if num is not None: num.status = self.status[key]
            sym = next((x for x in self.syms if x.title == key), None)
            if sym is not None: sym.status = self.status[key]


class LazyTable:
    def __init__(self, csvfile):
        self.nums = []
        self.syms = []
        self.isClass = {}
        self.goals = {}
        self.status = {}
        self.csvfile = csvfile
        self.csvRowsGenerator()
        self.readRowsLineByLine()
        self.setMeta()
        self.showStatistics()

    def csvRowsGenerator(self):
        with open(self.csvfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                yield row

    def readRowsLineByLine(self):
            # yield next(csv_reader)
            line_count = 1
            toBeIgnored = []
            toBeParsedToInt = []
            titles = []
            for row in self.csvRowsGenerator():
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
                            self.goals[item] = 'max'
                            self.status[item] = "dependent"
                        if '<' in item:
                            toBeParsedToInt.append(index)
                            self.goals[item] = 'min'
                            self.status[item] = "independent"
                        if '!' in item:
                            self.isClass[item] = True
                        if '%' in item:
                            pass
                    if index not in toBeIgnored:
                        if line_count == 1:
                            if index not in toBeParsedToInt:
                                self.syms.append(Sym.Sym(item, index))
                            if index in toBeParsedToInt:
                                self.nums.append(Num.Num(item, index))
                        else:
                            if index not in toBeParsedToInt:
                                sym = next((x for x in self.syms if x.title == titles[index]), None)
                                if '?' not in item:
                                    sym.increment(item)
                            if index in toBeParsedToInt:
                                num = next((x for x in self.nums if x.title == titles[index]), None)
                                if '?' not in item:
                                    num.increment(float(item))

                line_count += 1

    def showStatistics(self):
        print("(Id, title, total, mode, frequency)")
        for item in self.syms:
            print(f'({item.columnIndex}, {item.title}, {item.total}, {item.mode}, {item.most})')

        print("")

        print("(Id, title, total, mean, standard deviation)")
        for item in self.nums:
            print(f'({item.columnIndex}, {item.title}, {item.count}, {item.mean : 0.2f}, {item.sd : 0.2f})')

        print('---***---\n')

    def setMeta(self):
        for key in self.goals:
            # print(f'{key} -> {self.goals[key]}')
            num = next((x for x in self.nums if x.title == key), None)
            if num is not None: num.goal = self.goals[key]
        for key in self.isClass:
            # print(f'{key} -> {self.isClass[key]}')
            sym = next((x for x in self.syms if x.title == key), None)
            if sym is not None: sym.isClass = self.isClass[key]
        for key in self.status:
            # print(f'{key} -> {self.status[key]}')
            num = next((x for x in self.nums if x.title == key), None)
            if num is not None: num.status = self.status[key]
            sym = next((x for x in self.syms if x.title == key), None)
            if sym is not None: sym.status = self.status[key]
