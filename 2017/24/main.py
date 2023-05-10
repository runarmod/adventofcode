import re
from collections import defaultdict, deque


def parseLine(line):
    return tuple(map(int, re.findall(r"\d+", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        data = (parseLine(line) for line in open(filename).read().rstrip().split("\n"))
        self.data = defaultdict(set)
        for a, b in data:
            self.data[a].add(b)
            self.data[b].add(a)
        self.bridges = sorted(self.bfs(), key=lambda x: len(x))

    def bfs(self):
        q = deque([(0, {(0, value),}, []) for value in self.data[0]])
        while q:
            node, visited, history = q.popleft()
            yield history
            for neighbor in self.data[node]:
                bridge = tuple(sorted((node, neighbor)))
                if bridge in visited:
                    continue
                q.append((neighbor, visited.union({bridge,}), history + [(node, neighbor)]))

    def part1(self):
        return max(sum(sum(lst) for lst in history) for history in self.bridges)

    def part2(self):
        return max(
            sum(sum(lst) for lst in history)
            for history in filter(lambda x: len(x) == len(self.bridges[-1]), self.bridges)
        )


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
