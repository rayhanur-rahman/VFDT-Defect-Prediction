import TestRig, math, random, re
from collections import defaultdict, Counter
from functools import reduce


def test1():
    sum = 0
    for number in range(1, 10):
        sum = sum + number
    assert sum == 45


def test2():
    factorialOfFive = math.factorial(5)
    assert factorialOfFive == 120


def test3():
    number = 5 / 2
    assert number == 2.5


def areaOfSquare(r):
    return r * r


def test4():
    assert areaOfSquare(10) == 100


def test5():
    text = "hello world"
    lengthOfText = len(text)
    assert lengthOfText == 11


def test6():
    array = [0, 1, 2]
    isExecuted = True
    try:
        array[4] = 5
    except:
        isExecuted = False
    assert isExecuted == False


def test7():
    list = []
    for i in range(0, 10):
        list.append(i)
    assert list == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test8():
    firstName, lastName = ["John", "Doe"]
    assert firstName == "John"


def test9():
    origin = (0, 0)
    point = (4, 3)
    distanceFromOrigin = math.sqrt((origin[0] - point[0]) * (origin[0] - point[0]) \
                                   + (origin[1] - point[1]) * (origin[1] - point[1]))
    assert distanceFromOrigin == 5


def test10():
    passport = {
        "Name": "John Doe",
        "Number": "XY 000000",
        "DOB": "1-January-0000",
        "Country": "ANtartica"
    }

    assert passport["Name"] == "John Doe"


def test11():
    passport = {
        "Name": "John Doe",
        "Number": "XY 000000",
        "DOB": "1-January-0000",
        "Country": "ANtartica"
    }
    passport = defaultdict(lambda: "John Doe", passport)
    assert passport["email"] == "John Doe"


def test12():
    text = "the quick fox jumps over the lazy dog"
    list = []
    for char in text:
        list.append(char)
    characterCount = Counter(list)
    assert characterCount["t"] == 2


def test13():
    uniqueNumbers = set()
    for number in range(1, 1000):
        uniqueNumbers.add(random.randint(1, 5))
    print(uniqueNumbers)
    assert uniqueNumbers == {1, 2, 3, 4, 5}


def test14():
    list = []
    for number in range(0, 10):
        if number % 2 == 0:
            list.append(number)
    assert list == [0, 2, 4, 6, 8]


def test15():
    isNumberIsOdd = None
    number = 101
    number = number % 2
    if number == 1:
        isNumberIsOdd = True
    else:
        isNumberIsOdd = False
    assert isNumberIsOdd == True


def test16():
    passport = {
        "Name": "John Doe",
        "Number": "XY 000000",
        "DOB": "1-January-0000",
        "Country": "ANtartica",
        "Visas": ["Mars", "Sun"]
    }
    assert all(passport["Visas"]) == True


def test17():
    list = []
    for number in range(10, 0, -1):
        list.append(number)
    list.sort()
    assert list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test18():
    list = [n for n in range(0, 10) if n % 5 == 0]
    assert list == [0, 5]


def fibGenerator():
    f0 = 0
    f1 = 1
    fib = 0
    for number in range(1, 10):
        fib = f0 + f1
        f0 = f1
        f1 = fib
        yield fib


def test19():
    list = []
    for number in fibGenerator():
        list.append(number)
    assert list == [1, 2, 3, 5, 8, 13, 21, 34, 55]


def test20():
    possibleDayForTrip = ["SAT", "SUN", "MON", "TUE", "WED", "THU", "FRI"]
    randomlySelectedDay = random.choice(possibleDayForTrip)
    if randomlySelectedDay in possibleDayForTrip:
        assert 1 == 1
    else:
        assert 1 == 2


def test21():
    phoneNum1 = "919-000-9999"
    phoneNum2 = "919-444-666"
    pattern = "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"
    match = re.match(pattern, phoneNum1)
    if match:
        assert 1 == 1
    match = re.match(pattern, phoneNum2)
    if not match:
        assert 1 == 1


class Point:
    point = (3, 4)
    origin = (0, 0)

    def getDistanceOfPoint(self):
        return math.sqrt((self.origin[0] - self.point[0]) * (self.origin[0] - self.point[0]) \
                         + (self.origin[1] - self.point[1]) * (self.origin[1] - self.point[1]))


def test22():
    p = Point()
    assert p.getDistanceOfPoint() == 5


def cube(n):
    return n * n * n


def test23():
    numbers = (1, 2, 3, 4)
    result = list(map(cube, numbers))
    print(result)
    assert result == [1, 8, 27, 64]


def test24():
    text = ['it', 'is', 'very', 'cold', 'in', 'the', 'Antarctica']
    appendedText = reduce((lambda text1, text2: text1 + ' ' + text2), text)
    assert appendedText == 'it is very cold in the Antarctica'


def test25():
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    monthsWithIndex = list(enumerate(months, 1))
    assert monthsWithIndex[0][0] == 1


def test26():
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    monthsWithIndex = list(zip(numbers, months))
    assert monthsWithIndex[0][0] == 1


def concatenateWords(*args):
    text = ''
    for word in args:
        text = text + word
    return text


def test27():
    assert concatenateWords('hello', 'good', 'morning') == 'hellogoodmorning'


TestRig.O.k(test1)
TestRig.O.k(test2)
TestRig.O.k(test3)
TestRig.O.k(test4)
TestRig.O.k(test5)
TestRig.O.k(test6)
TestRig.O.k(test7)
TestRig.O.k(test8)
TestRig.O.k(test9)
TestRig.O.k(test10)
TestRig.O.k(test11)
TestRig.O.k(test12)
TestRig.O.k(test13)
TestRig.O.k(test14)
TestRig.O.k(test15)
TestRig.O.k(test16)
TestRig.O.k(test17)
TestRig.O.k(test18)
TestRig.O.k(test19)
TestRig.O.k(test20)
TestRig.O.k(test21)
TestRig.O.k(test22)
TestRig.O.k(test23)
TestRig.O.k(test24)
TestRig.O.k(test25)
TestRig.O.k(test26)
TestRig.O.k(test27)

if __name__ == '__main__':
    TestRig.O.report()
