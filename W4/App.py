import Config, Sample, math, random, Num, Sym, Rows, csv

random.seed(0)

print('---statistics of weather Load All into RAM---')
csv_reader = Rows.Table("weather.csv")

print('---statistics of weather long Load All into RAM---')
csv_reader = Rows.Table("weatherLong.csv")

print('---statistics of auto Load All into RAM---')
csv_reader = Rows.Table("auto.csv")


print('---statistics of weather Load Sequentially from Secondary Memory---')
csv_reader = Rows.LazyTable("weather.csv")

print('---statistics of weather long Load Sequentially from Secondary Memory---')
csv_reader = Rows.LazyTable("weatherLong.csv")

print('---statistics of auto Load Sequentially from Secondary Memory---')
csv_reader = Rows.LazyTable("auto.csv")



