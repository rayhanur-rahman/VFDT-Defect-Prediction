import sys
sys.path.insert(0, '../W3/')

import Config, Sample, math, random, Num, Sym, Rows

print('---using yield & generator---')
print('---it does not load the whole data to RAM---')
print('---but it is supposed to load all the pointers to RAM---\n')
print('---statistics of weather---')
table = Rows.TableLoader('weather.csv')
table.loadTableWithGenerator()

print('---statistics of weather long---')
table = Rows.TableLoader('weatherLong.csv')
table.loadTableWithGenerator()

print('---statistics of auto---')
table = Rows.TableLoader('auto.csv')
table.loadTableWithGenerator()

print('---using standard IO---')
print('---it does not load the whole data to RAM---')
print('---t is supposed to load only one line to RAM---\n')

print('---statistics of weather---')
table = Rows.TableLoader('weather.csv')
table.loadTableWithStandardInput()

print('---statistics of weather long---')
table = Rows.TableLoader('weatherLong.csv')
table.loadTableWithStandardInput()

print('---statistics of auto---')
table = Rows.TableLoader('auto.csv')
table.loadTableWithStandardInput()

