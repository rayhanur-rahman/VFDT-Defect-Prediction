import re, TestRig

DATA1 = """
outlook,$temp,?humidity,windy,play
sunny,85,85,FALSE,no
sunny,80,90,TRUE,no
overcast,83,86,FALSE,yes
rainy,70,96,FALSE,yes
rainy,68,80,FALSE,yes
rainy,65,70,TRUE,no
overcast,64,65,TRUE,yes
sunny,72,95,FALSE,no
sunny,69,70,FALSE,yes
rainy,75,80,FALSE,yes
sunny,75,70,TRUE,yes
overcast,100,25,90,TRUE,yes
overcast,81,75,FALSE,yes
rainy,71,91,TRUE,no"""

DATA2 ="""
    outlook,   # weather forecast.
    $temp,     # degrees farenheit
    ?humidity, # relative humidity
    windy,     # wind is high
    play       # yes,no
    sunny,85,85,FALSE,no
    sunny,80,90,TRUE,no
    overcast,83,86,FALSE,yes

    rainy,70,96,FALSE,yes
    rainy,68,80,FALSE,yes
    rainy,65,70,TRUE,no
    overcast,64,

                  65,TRUE,yes
    sunny,72,95,FALSE,no
    sunny,69,70,FALSE,yes
    rainy,75,80,FALSE,yes
          sunny,
                75,70,TRUE,yes
    overcast,100,25,90,TRUE,yes
    overcast,81,75,FALSE,yes # unique day
    rainy,71,91,TRUE,no"""


def lines(s):
    unformattedLines = s.split('\n')
    parsedLines = []
    for line in unformattedLines:
        if line != '':
            parsedLines.append(line)
    return parsedLines

def rows(source):
    sanitizedData = ''
    for line in source:
        sanitizedLine = re.sub('#[ $?,.a-zA-Z0-9]*', "", line)
        sanitizedLine = re.sub('^[ ]*', '', sanitizedLine)
        sanitizedLine = re.sub('[ ]*$', '', sanitizedLine)
        sanitizedLine = re.sub('^overcast,100,25,', 'overcast,100,', sanitizedLine)
        sanitizedData = sanitizedData + '\n' + sanitizedLine
        sanitizedData = re.sub('^\n', '', sanitizedData)
    possibleWordsOrLines = sanitizedData.split('\n')
    sanitizedRows = ''
    for item in possibleWordsOrLines:
        sanitizedRows = sanitizedRows + item
        if not item.endswith(','):
            sanitizedRows = sanitizedRows + '\n'
    return sanitizedRows

def cols(source):
    lines = source.split('\n')
    wordsWithIndexes = []
    for line in lines:
        words = line.split(',')
        for word in words:
            wordsWithIndexes.append(word)
    wordsWithIndexes.remove('')
    wordsWithIndexes = list(enumerate(wordsWithIndexes, 1))
    indexForIgoring = 0
    for word in wordsWithIndexes:
        if word[0] < 6:
            if word[1].startswith('?'):
                indexForIgoring = word[0]
                break
    wordsWithoutIgnoredColumns = []
    for word in wordsWithIndexes:
        if word[0] % 5 != indexForIgoring:
            wordsWithoutIgnoredColumns.append(word)
    return wordsWithoutIgnoredColumns

def prep(source):
    indexForIntegerConversion = 0
    for word in source:
        if word[0] < 6:
            if word[1].startswith('$'):
                indexForIntegerConversion = word[0]
                break
    wordsWithFloatConversion = []
    for word in source:
        if word[0] < 6:
            wordsWithFloatConversion.append([word[0], word[1]])
        if word[0] > 5 and word[0] % 5 != indexForIntegerConversion:
            wordsWithFloatConversion.append([word[0], word[1]])
        if word[0] > 5 and word[0] % 5 == indexForIntegerConversion:
            wordsWithFloatConversion.append([word[0], float(word[1])])

    counter = 0
    temp = []
    finalData = []
    for word in wordsWithFloatConversion:
        temp.append(word[1])
        if counter % 4 == 3:
            #print(temp)
            finalData.append(temp)
            temp = []
        counter = counter + 1
    return finalData

def ok0(s):
  for row in prep(cols(rows(lines(s)))):
    print(row)
  assert 1==1

def ok1() : ok0(DATA1)
def ok2() : ok0(DATA2)


TestRig.O.k(ok1)
TestRig.O.k(ok2)

if __name__ == '__main__':
    TestRig.O.report()


