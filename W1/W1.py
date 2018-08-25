import TestRig, math, random
from collections import defaultdict, Counter


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
    for number in range(0,10):
        if number % 2 == 0:
            list.append(number)
    assert list == [0,2,4,6,8]

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
        "Visas" : ["Mars", "Sun"]
    }
    assert all(passport["Visas"]) == True

def test17():
    list = []
    for number in range(10,0,-1):
        list.append(number)
    list.sort()
    assert list == [1,2,3,4,5,6,7,8,9,10]

def test18():
    list = [n for n in range(0,10) if n % 5 == 0]
    assert list == [0,5]

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

if __name__ == '__main__':
    TestRig.O.report()
