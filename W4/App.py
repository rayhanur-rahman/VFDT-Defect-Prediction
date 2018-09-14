import Config, Sample, math, random, Num, Sym, Rows

random.seed(0)

print('---statistics of weather---')
csv = Rows.CSVDataImporter("weather.csv")
csv.showStatistics()
print('---###---\n')

print('---statistics of weather long---')
csv = Rows.CSVDataImporter("weatherLong.csv")
csv.showStatistics()
print('---###---\n')

print('---statistics of auto---')
csv = Rows.CSVDataImporter("auto.csv")
csv.showStatistics()
print('---###---\n')