from collections import Counter
import re


def parseLine(line):
    name, weight, children = re.findall(r"(\w+) \((\d+)\)(?: -> ([\w, ]+))?", line)[0]
    weight = int(weight)
    children = set(children.split(", ")) if children else set()
    return name, weight, children


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = map(parseLine, open(filename).read().rstrip().split("\n"))

        self.weights = {}
        self.children = {}
        self.parent = {}
        for name, weight, children in self.data:
            self.weights[name] = weight
            self.children[name] = children
            for child in children:
                self.parent[child] = name

    def part1(self):
        for _, parent in self.parent.items():
            if parent not in self.parent.keys():
                self.bottom = parent
                return parent
        return None

    def weight(self, node):
        return self.weights[node] + sum(self.weight(node) for node in self.children[node])

    def find_correct_weight(self, node):
        counter = Counter(self.weight(child) for child in self.children[node])
        if len(counter) == 1:
            return False

        least = counter.most_common()[-1][0]
        for child in self.children[node]:
            if self.weight(child) == least:
                wrong_node = child
                break

        return (
            answer
            if (answer := self.find_correct_weight(wrong_node))
            else counter.most_common()[0][0] - (self.weight(wrong_node) - self.weights[wrong_node])
        )

    def part2(self):
        return self.find_correct_weight(self.bottom)


def main():
    test = Solution(test=True)
    print(f"(Test) Part 1: {test.part1()}")
    print(f"(Test) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
