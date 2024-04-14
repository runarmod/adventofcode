import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(filename).read().rstrip()
        self.map = dict(zip("^>v<", (1j, 1, -1j, -1)))

    def part1(self):
        pos = 0j
        visited = {pos}
        for direction in self.data:
            pos += self.map[direction]
            visited.add(pos)
        return len(visited)

    def part2(self):
        pos = [0j, 0j]
        visited = {pos[0]}
        for i, direction in enumerate(self.data):
            pos[i % 2] += self.map[direction]
            visited.add(pos[i % 2])
        return len(visited)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 11 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
