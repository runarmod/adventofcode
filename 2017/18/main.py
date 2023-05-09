from itertools import count
import time
from collections import defaultdict, deque


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = [line.split(" ") for line in open(filename).read().rstrip().split("\n")]

    def part1(self):
        registers = defaultdict(int)
        last_played_value = None

        i = 0
        while 0 <= i < len(self.data):
            cmd = self.data[i][:]
            if len(cmd) == 3 and cmd[2].isalpha():
                cmd[2] = registers[cmd[2]]

            match cmd[0]:
                case "snd":
                    last_played_value = registers[cmd[1]]
                case "set":
                    registers[cmd[1]] = int(cmd[2])
                case "add":
                    registers[cmd[1]] += int(cmd[2])
                case "mul":
                    registers[cmd[1]] *= int(cmd[2])
                case "mod":
                    registers[cmd[1]] %= int(cmd[2])
                case "rcv":
                    if registers[cmd[1]] != 0:
                        return last_played_value
                case "jgz":
                    if registers[cmd[1]] > 0:
                        i += int(cmd[2])
                        continue
            i += 1
        return None

    def machine(self, _id, this_queue, other_queue):
        registers = defaultdict(int)
        registers["p"] = _id
        send_count = 0

        def val(value):
            return registers[value] if value.isalpha() else int(value)

        i = 0
        while i < len(self.data):
            cmd, *args = self.data[i][:]
            if len(args) == 2:
                a, b = args
            else:
                a = args[0]

            match cmd:
                case "snd":
                    other_queue.append(val(a))
                    send_count += 1
                case "set":
                    registers[a] = val(b)
                case "add":
                    registers[a] += val(b)
                case "mul":
                    registers[a] *= val(b)
                case "mod":
                    registers[a] %= val(b)
                case "rcv":
                    if len(this_queue) > 0:
                        registers[a] = this_queue.popleft()
                    else:
                        i -= 1
                        yield False, send_count
                case "jgz":
                    if val(a) > 0:
                        i += val(b) - 1
            i += 1
            yield True, send_count
        yield False, send_count

    def part2(self):
        queue0 = deque()
        queue1 = deque()
        machine0 = self.machine(0, queue0, queue1)
        machine1 = self.machine(1, queue1, queue0)

        start = time.time()
        for i in count():
            more0, _ = next(machine0)
            more1, send_count1 = next(machine1)
            if i % 1000 == 0 and time.time() - start > 5:
                break
            """
            The "if" below does not work since it is in infinity loop.
            If it has run for more than 5 seconds, we are
            probably in a loop, so break
            """
            if not more0 and not more1:
                break
        return send_count1


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
