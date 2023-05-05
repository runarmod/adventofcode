class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = tuple(map(int, open(filename).read().rstrip().split(" ")))
        self.run()

    def run(self):
        self.i = 0
        self.part1_answer = 0

        def parse_node():
            child_count, metadata_count = self.data[self.i : self.i + 2]
            self.i += 2
            children_score = [parse_node() for _ in range(child_count)]

            metadatas = self.data[self.i : self.i + metadata_count]
            self.part1_answer += (sum_metadata := sum(metadatas))
            self.i += metadata_count

            if child_count == 0:
                return sum_metadata

            _sum = 0
            for index in metadatas:
                if 0 < index <= child_count:
                    _sum += children_score[index - 1]
            return _sum

        self.part2_answer = parse_node()

    def part1(self):
        return self.part1_answer

    def part2(self):
        return self.part2_answer


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
