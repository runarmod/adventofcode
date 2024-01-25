import time


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(int, open(filename).read().rstrip()))

    def get_next3(self, current, cup_neighbours):
        next3 = [cup_neighbours[current]]
        next3.append(cup_neighbours[next3[-1]])
        next3.append(cup_neighbours[next3[-1]])
        return next3

    def get_final_neighbours(self, cups: list[int], steps: int):
        # Could use dict, but list is faster when we have unique
        # sequential, no gap, numbers for 1 to x
        cup_neighbours = [-1 for _ in range(len(cups) + 1)]
        for cup, neighbour in zip(cups, cups[1:] + cups[:1]):
            cup_neighbours[cup] = neighbour

        minimum, maximum = min(cups), max(cups)
        current = cups[0]

        for _ in range(steps):
            next3 = self.get_next3(current, cup_neighbours)

            # Get the destition
            destination = current - 1
            while destination in next3 or destination < minimum:
                destination = maximum if destination <= minimum else destination - 1

            # Current cup should point at the cup past the tripple
            cup_neighbours[current] = cup_neighbours[next3[-1]]
            # The last cup in the tripple should point to the cup past the destination
            cup_neighbours[next3[-1]] = cup_neighbours[destination]
            # The destination should point to the tripple
            cup_neighbours[destination] = next3[0]

            current = cup_neighbours[current]
        return cup_neighbours

    def get_answer(self, neighbours: list[int]):
        out = 0
        current = neighbours[1]
        while current != 1:
            out = out * 10 + current
            current = neighbours[current]
        return out

    def part1(self) -> int:
        cups = [c for c in self.data]
        neighbours = self.get_final_neighbours(cups, 100)
        return self.get_answer(neighbours)

    def multiply_2_children(self, parent: int, neighbours: list[int]):
        first = neighbours[parent]
        second = neighbours[first]
        return first * second

    def part2(self) -> int:
        cups = self.data + list(range(len(self.data) + 1, 1_000_001))
        neighbours = self.get_final_neighbours(cups, 10_000_000)
        return self.multiply_2_children(1, neighbours)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 67384529 else 'wrong :('}"
    )
    test2 = test.part2()
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 149245887792 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
