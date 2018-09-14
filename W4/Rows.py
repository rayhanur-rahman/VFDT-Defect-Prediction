import csv,sys, Num, Sym

class CSVDataImporter:
    def __init__(self, csvfile):
        self.nums = []
        self.syms = []

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
                        if '<' in item:
                            toBeParsedToInt.append(index)
                    if index not in toBeIgnored:
                        if line_count == 1:
                            if index not in toBeParsedToInt:
                                self.syms.append(Sym.Sym(item))
                            if index in toBeParsedToInt:
                                self.nums.append(Num.Num(item))
                        else:
                            if index not in toBeParsedToInt:
                                sym = next((x for x in self.syms if x.title == titles[index]), None)
                                sym.increment(item)
                            if index in toBeParsedToInt:
                                num = next((x for x in self.nums if x.title == titles[index]), None)
                                if '?' not in item:
                                    num.increment(float(item))

                line_count += 1
        return

    def showStatistics(self):
        print("(title, total, mode, frequency)")
        for item in self.syms:
            print(f'({item.title}, {item.total}, {item.mode}, {item.most})')

        print("")

        print("(title, total, mean, standard deviation)")
        for item in self.nums:
            print(f'({item.title}, {item.count}, {item.mean : 0.2f}, {item.sd : 0.2f})')

