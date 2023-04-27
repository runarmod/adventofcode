import re


def parseLine(line):
    if "mask" in line:
        return (line.split(" ")[-1],)
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]

    def getValueV1(self, mask, value):
        _mask = mask
        _value = list(bin(value)[2:].zfill(36))
        for i in range(36):
            if _mask[i] != "X":
                _value[i] = _mask[i]
        return int("".join(_value), 2)

    def part1(self):
        memory = {}
        mask = "X" * 36
        for line in self.data:
            if len(line) == 1:
                mask = line[0]
                continue
            memory[line[0]] = self.getValueV1(mask, line[1])
        return sum(val for _, val in memory.items())

    def calculate(self, mask, address, value):
        addressBin = list(bin(address)[2:].zfill(36))
        for i in range(36):
            if mask[i] != "0":
                addressBin[i] = mask[i]
        self.writeToMemory("".join(addressBin), value)

    def writeToMemory(self, address, value):
        addresses = [address]
        while addresses[0].find("X") != -1:
            _addresses = []
            for _address in addresses:
                _addresses += [_address.replace("X", "0", 1), _address.replace("X", "1", 1)]
            addresses = _addresses

        for address in addresses:
            self.memory[int(address, 2)] = value

    def part2(self):
        self.memory = {}
        mask = "X" * 36
        for line in self.data:
            if len(line) == 1:
                mask = line[0]
                continue
            self.calculate(mask, line[0], line[1])
        return sum(self.memory.values())


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
