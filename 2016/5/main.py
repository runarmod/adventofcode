import hashlib
import random
from tqdm import trange

inn = "ffykfhsq"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Part1:
    def __init__(self):
        self.password = ""
        i = -1
        for _ in range(8):
            while True:
                i += 1
                result = hashlib.md5((inn + str(i)).encode()).hexdigest()
                if result[:5] == "0" * 5:
                    print("First character:", result[6], "from", result, "with i", i)
                    self.password += result[5]
                    break


class Part2:
    def __init__(self):
        self.password = ["_"] * 8
        self.invalid_positions = []
        i = -1
        j = 0
        while True:
            i += 1
            result = hashlib.md5((inn + str(i)).encode()).hexdigest()
            if result[:5] == "0" * 5:
                if result[5].isdigit():
                    if int(result[5]) not in self.invalid_positions and int(result[5]) in range(0,8):
                        self.password[int(result[5])] = result[6]
                        # print("".join(self.password))
                        self.invalid_positions.append(int(result[5]))
                        j += 1
                        if j == 8:
                            break
            if i % 30000 == 0:
                for char in self.password:
                    if char == '_':
                        print(bcolors.HEADER + str(random.random())[-1] + bcolors.ENDC, end='')
                    else:
                        print(bcolors.OKGREEN + char + bcolors.ENDC, end='')
                print('\r', end='')
        self.password = "".join(self.password)

# part1 = Part1()
# print("Part 1:", part1.password)


part2 = Part2()
print("Part 2:", part2.password)