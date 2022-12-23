from collections import defaultdict
import itertools


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"

    def reset(self):
        self.wishes = defaultdict(set)
        grid = list(map(list, open(self.filename).read().rstrip().split("\n")))
        self.pos = set()
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "#":
                    self.pos.add((j, i))

    def has_neighbours(self, x, y):
        for dx, dy in itertools.product((-1, 0, 1), repeat=2):
            if dx == dy == 0:
                continue
            if (x + dx, y + dy) in self.pos:
                return True
        return False

    def act_on_wishes(self):
        for new_pos, old_poses in self.wishes.items():
            if len(old_poses) == 1:
                self.pos.add(new_pos)
                self.pos.remove(old_poses.pop())
        self.wishes.clear()

    def empty_in_square_count(self):
        # Size of rectangle, minus elf count
        minx = min(x for x, _ in self.pos)
        miny = min(y for _, y in self.pos)
        maxx = max(x for x, _ in self.pos)
        maxy = max(y for _, y in self.pos)
        return (maxx - minx + 1) * (maxy - miny + 1) - len(self.pos)

    def remove_unwanted_directions(self, x, y, considered):
        for d in (-1, 0, 1):
            if (x + d, y - 1) in self.pos:
                considered[0] = False
            if (x + d, y + 1) in self.pos:
                considered[1] = False
            if (x - 1, y + d) in self.pos:
                considered[2] = False
            if (x + 1, y + d) in self.pos:
                considered[3] = False

    def add_wish_from_considerations(self, round, x, y, considered):
        dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for i in range(len(considered)):
            if considered[(round + i) % len(considered)]:
                dx, dy = dirs[(round + i) % len(considered)]
                self.wishes[(x + dx, y + dy)].add((x, y))
                break

    def generate_wishes(self, round):
        for x, y in self.pos:
            # If no neighbours, no movement
            if not self.has_neighbours(x, y):
                continue
            considered = [True for _ in range(4)]  # N S W E

            # Remove directions that has an elf
            self.remove_unwanted_directions(x, y, considered)

            self.add_wish_from_considerations(round, x, y, considered)

    def part1(self):
        self.reset()
        for round_nr in range(10):
            self.generate_wishes(round_nr)
            self.act_on_wishes()
        return self.empty_in_square_count()

    def part2(self):
        self.reset()
        round_nr = 0
        while True:
            self.generate_wishes(round_nr)
            if len(self.wishes) == 0:
                break
            self.act_on_wishes()
            round_nr += 1
        return round_nr + 1


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
