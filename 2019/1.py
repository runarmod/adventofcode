import requests
from adventofcodeCookie import aoc_cookie

inn = [int(i) for i in requests.get("https://adventofcode.com/2019/day/1/input", cookies=aoc_cookie).text.split()]
# inn = [int(i) for i in open("test.txt").read().split()]

def part1():
    s = 0
    for i in inn:
        s += i // 3 - 2
    print("Part 1:", s)

def part2():
    s = 0
    for i in inn:
        additional = i // 3 - 2
        s += additional
        # print(s)
        while True:
            additional = additional // 3 - 2
            if additional <= 0:
                break
            else:
                s += additional
    print("Part 2:", s)

# part1()
part2()