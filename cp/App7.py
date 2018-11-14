import csv, re, Utils, math, sys, Node, timeit


def dump(csvFile):
    streamIndex = 0
    file = open('dump.csv', 'w')
    for row in Utils.csvRowsGenerator(csvFile):
        streamIndex = streamIndex + 1
        if streamIndex % 100000 == 0:
            print(f'{streamIndex} lines done')
        if streamIndex <= 8800000:
            continue

        line = ''
        for col in row:
            if len(line) == 0: line = line + col
            else: line = line + ',' + col
        file.write(line+'\n')

    file.close()
    return

dump('/media/rr/8E30E13030E12047/bigdata/higgs.csv')

