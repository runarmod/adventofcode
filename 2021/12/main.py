import functools
from collections import defaultdict, deque


def parseLine(line):
    return line.split("-")


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]
        self.map = defaultdict(list)
        self.generate_map()

    def generate_map(self):
        for start, end in self.data:
            self.map[start].append(end)
            self.map[end].append(start)

    def part1(self):
        paths = []
        bfs = deque()
        bfs.append(("start", {"start"}))
        while bfs:
            cave, visited = bfs.popleft()
            for option in self.map[cave]:
                if option == "end":
                    paths.append(visited)
                    continue
                if option.islower() and option in visited:
                    continue
                bfs.append((option, visited.union({option})))
        return len(paths)

    def part2(self):
        self.paths = 0
        self.paths = self.count("start", frozenset(("start",)), True)
        return self.paths

    @functools.lru_cache(maxsize=None)
    def count(self, cave, visited, can_do_one_twice):
        paths = 0
        for target in self.map[cave]:
            if target == "start":
                continue
            if target == "end":
                paths += 1
                continue
            if target not in visited or target.isupper():
                paths += self.count(target, visited.union({target}), can_do_one_twice)
                continue
            if can_do_one_twice:
                paths += self.count(target, visited.union({target}), False)
        return paths


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")
    part2 = solution.part2()
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
