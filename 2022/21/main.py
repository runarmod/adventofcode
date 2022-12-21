class Monkey:
    def __init__(self, name, op):
        global monkeys
        self.name = name
        self.value = None
        self.operation = None
        if all(o not in op for o in "+/*-"):
            self.value = int(op)
            return
        self.first, self.operation, self.last = op.split(" ")

    def children_equal(self):
        first, second = monkeys[self.first].get_value(), monkeys[self.last].get_value()
        if first == second:
            return 0
        return -1 if first < second else 1

    def get_value(self):
        if self.value is not None:
            return self.value

        if self.operation == "*":
            self.value = (
                monkeys[self.first].get_value() * monkeys[self.last].get_value()
            )
        elif self.operation == "+":
            self.value = (
                monkeys[self.first].get_value() + monkeys[self.last].get_value()
            )
        elif self.operation == "-":
            self.value = (
                monkeys[self.first].get_value() - monkeys[self.last].get_value()
            )
        elif self.operation == "/":
            self.value = (
                monkeys[self.first].get_value() / monkeys[self.last].get_value()
            )
        else:
            raise NotImplementedError("WHAT")

        return self.value

    def set_value(self, value):
        self.value = value

    def reset_value(self):
        if self.operation:
            self.value = None

    def set_has_human_under(self):
        if self.name == "humn":
            self.has_human_under = True
            return True
        if self.operation is None:
            return False
        if any(
            (
                monkeys[self.first].set_has_human_under(),
                monkeys[self.last].set_has_human_under(),
            )
        ):
            self.has_human_under = True
            return True
        self.has_human_under = False
        return False

    def write_to_file(self):
        if self.value is not None:
            return "x" if self.name == "humn" else str(self.value)
        if self.name == "root":
            return f"{monkeys[self.first].write_to_file()}={monkeys[self.last].write_to_file()}"
        return f"({monkeys[self.first].write_to_file()}{self.operation}{monkeys[self.last].write_to_file()})"

    def __repr__(self):
        return self.name


def parseLine(line):
    monkey, op = line.split(": ")
    return (monkey, Monkey(monkey, op))


monkeys = {}


class Solution:
    global monkeys

    def __init__(self):
        self.filename = "input.txt"

    def get_fresh_monkeys(self):
        global monkeys
        monkeys = {}
        for line in open(self.filename).read().rstrip().split("\n"):
            key, val = parseLine(line)
            monkeys[key] = val
        with open("out.txt", "w") as f:
            out = monkeys["root"].write_to_file()
            f.write(out)

    def set_all_has_human_under(self):
        global monkeys
        self.need_update = set()
        for _, val in monkeys.items():
            if val.set_has_human_under():
                self.need_update.add(val)

    def reset_values(self):
        for monkey in self.need_update:
            monkey.reset_value()

    def part1(self):
        self.get_fresh_monkeys()
        return int(monkeys["root"].get_value())

    def part2(self):
        global monkeys
        self.get_fresh_monkeys()
        self.set_all_has_human_under()
        l = 0
        r = 5_000_000_000_000
        while True:
            self.reset_values()
            i = (r + l) // 2
            monkeys["humn"].set_value(i)
            ret = monkeys["root"].children_equal()
            if ret == -1:
                r = i - 1
            elif ret == 0:
                return i
            elif ret == 1:
                l = i + 1


def main():
    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
