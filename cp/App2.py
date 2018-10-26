import csv


def csvRowsGenerator(csvfile):
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            yield row

def readRowsLineByLine(csvfile):
    for row in csvRowsGenerator(csvfile):
        print(float(row[1]))


readRowsLineByLine("D:\\bigdata\\higgs.csv")


