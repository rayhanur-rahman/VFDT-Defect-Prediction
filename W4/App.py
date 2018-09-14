import Config, Sample, math, random, Num, Sym, Rows, csv

random.seed(0)

print('---statistics of weather Load All into RAM---')
csv_reader = Rows.CSVDataImporterAtOnce("weather.csv")

print('---statistics of weather long Load All into RAM---')
csv_reader = Rows.CSVDataImporterAtOnce("weatherLong.csv")

print('---statistics of auto Load All into RAM---')
csv_reader = Rows.CSVDataImporterAtOnce("auto.csv")


print('---statistics of weather Load Sequentially from Secondary Memory---')
csv_reader = Rows.CSVDataImporterSequential("weather.csv")

print('---statistics of weather long Load Sequentially from Secondary Memory---')
csv_reader = Rows.CSVDataImporterSequential("weatherLong.csv")

print('---statistics of auto Load Sequentially from Secondary Memory---')
csv_reader = Rows.CSVDataImporterSequential("auto.csv")



