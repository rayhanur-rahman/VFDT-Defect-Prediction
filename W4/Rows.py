import sys
sys.path.insert(0, '../W3/')

import csv, Num, Sym, math

class TableLoader:
    def __init__(self, csvfile):
        self.nums = []
        self.syms = []
        self.isClass = {}
        self.goals = {}
        self.status = {}
        self.csvfile = csvfile

        self.line_count = 1
        self.toBeIgnored = []
        self.toBeParsedToInt = []
        self.titles = []

        self.listOfDataAsDictionary = []

    def processLine(self, row):
        dictionary = {}
        for index in range(0, len(row)):
            item = row[index].strip()
            item = item.replace('\n', '')
            if self.line_count == 1:
                self.titles.append(item)
                if '?' in item:
                    self.toBeIgnored.append(index)
                else:
                    if '$' in item:
                        self.toBeParsedToInt.append(index)
                        self.status[item] = "independent"
                    if '>' in item:
                        self.toBeParsedToInt.append(index)
                        self.goals[item] = 'max'
                        self.status[item] = "dependent"
                    if '<' in item:
                        self.toBeParsedToInt.append(index)
                        self.goals[item] = 'min'
                        self.status[item] = "dependent"
                    if '!' in item:
                        self.isClass[item] = True
                    if '%' in item:
                        pass
            if index not in self.toBeIgnored:
                if self.line_count == 1:
                    if index not in self.toBeParsedToInt:
                        self.syms.append(Sym.Sym(item, index))
                    if index in self.toBeParsedToInt:
                        self.nums.append(Num.Num(item, index))
                else:
                    if index not in self.toBeParsedToInt:
                        sym = next((x for x in self.syms if x.title == self.titles[index]), None)
                        dictionary[self.titles[index]] = item
                        if '?' not in item:
                            sym.increment(item)
                    if index in self.toBeParsedToInt:
                        num = next((x for x in self.nums if x.title == self.titles[index]), None)
                        if '?' not in item:
                            num.increment(float(item))
                            dictionary[self.titles[index]] = float(item)
                        else:
                            dictionary[self.titles[index]] = item
        return dictionary

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

    def openFile(self, csvfile):
        with open(csvfile) as file:
            line = file.readline()
            while line:
                row = line.split(",")
                self.processLine(row)
                self.line_count += 1
                line = file.readline()
        self.setMeta()
        # self.showStatistics()

    def csvRowsGenerator(self):
        with open(self.csvfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                yield row

    def readRowsLineByLine(self):
        for row in self.csvRowsGenerator():
            dictionary = self.processLine(row)
            if len(dictionary) > 0: self.listOfDataAsDictionary.append(dictionary)
            self.line_count += 1

    def loadTableWithGenerator(self):
        self.csvRowsGenerator()
        self.readRowsLineByLine()
        self.setMeta()
        # self.showStatistics()

    def loadTableWithStandardInput(self):
        self.openFile(self.csvfile)

