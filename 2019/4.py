import requests
from adventofcodeCookie import aoc_cookie
from tqdm import trange

inn = [int(num) for num in requests.get("https://adventofcode.com/2019/day/4/input", cookies=aoc_cookie).text.split("-")]
inn = range(inn[0], inn[1] + 1)

def doubleIsTriple(i, indexOfDouble):
    i = str(i)
    for j in range(4):
        if i[j] == i[j + 1] and i[j + 1] == i[j + 2]:
            if indexOfDouble == j:
                return True
    return False


def doubleDigits(i):
    i = str(i)
    for j in range(5):
        if i[j] == i[j + 1]:
            return j


def increase(i):
    for j, k in zip(str(i), str(i)[1:]):
        if k < j:
            return False
    return True


def part1():
    count = 0
    for i in inn:
        if len(str(i)) != 6:
            continue
        if not increase(i):
            continue
        if doubleDigits(i) == None:
            continue
        count += 1
    print("Part 1:", count)


def part2():
    count = 0
    for i in inn:
        if len(str(i)) != 6:
            continue
        doubleIndex = doubleDigits(i)
        if doubleIndex == None:
            continue
        if doubleIsTriple(i, doubleIndex):
            continue
        # print(doubleIndex, trippleIndex, i)
        # if trippleIndex == doubleIndex:
        #     continue
        if not increase(i):
            continue
        count += 1
    print("Part 2:", count)


part1()
part2()