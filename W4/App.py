import Config, Sample, math, random, Num, Sym, Rows, prettytable

print('---using yield & generator---')
print('---it does not load the whole data to RAM---')
print('---but it is supposed to load all the pointers to RAM---\n')
print('---statistics of weather---')
table = Rows.TableLoader('weather.csv')
table.loadTableWithGenerator()
table.showStatistics()

print('---statistics of weather long---')
table = Rows.TableLoader('weatherLong.csv')
table.loadTableWithGenerator()
table.showStatistics()
table.showStatistics()


print('---statistics of auto---')
table = Rows.TableLoader('auto.csv')
table.loadTableWithGenerator()
table.showStatistics()

print('---using standard IO---')
print('---it does not load the whole data to RAM---')
print('---it is supposed to load only one line to RAM---\n')

print('---statistics of weather---')
table = Rows.TableLoader('weather.csv')
table.loadTableWithStandardInput()
table.showStatistics()

print('---statistics of weather long---')
table = Rows.TableLoader('weatherLong.csv')
table.loadTableWithStandardInput()
table.showStatistics()

print('---statistics of auto---')
table = Rows.TableLoader('auto.csv')
table.loadTableWithStandardInput()
table.showStatistics()

