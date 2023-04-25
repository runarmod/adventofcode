import itertools


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [list(line) for line in open(filename).read().rstrip().split("\n")]

    def adjacent_seat_occupied_count(self, seat_map, x, y, part):
        return self.adj_count_1(seat_map, x, y) if part == 1 else self.adj_count_2(seat_map, x, y)

    def adj_count_1(self, seat_map, x, y):
        count = 0
        for new_x, new_y in itertools.product(
            range(max((0, x - 1)), min((len(seat_map[0]), x + 2))),
            range(max((0, y - 1)), min((len(seat_map), y + 2))),
        ):
            if (new_x, new_y) == (x, y):
                continue
            if seat_map[new_y][new_x] == "#":
                count += 1
        return count

    def adj_count_2(self, seat_map, x, y):
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == dx == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                while 0 <= new_x < len(seat_map[0]) and 0 <= new_y < len(seat_map):
                    if seat_map[new_y][new_x] == "#":
                        count += 1
                        break
                    if seat_map[new_y][new_x] == "L":
                        break
                    new_x += dx
                    new_y += dy
        return count

    def one_round(self, data, part):
        new_data = []
        for y, line in enumerate(data):
            new_line = []
            for x, seat in enumerate(line):
                if seat == ".":
                    new_line.append(".")
                    continue
                if seat == "L":
                    if self.adjacent_seat_occupied_count(data, x, y, part) == 0:
                        new_line.append("#")
                    else:
                        new_line.append("L")
                    continue
                if seat == "#":
                    if self.adjacent_seat_occupied_count(data, x, y, part) >= (
                        4 if part == 1 else 5
                    ):
                        new_line.append("L")
                    else:
                        new_line.append("#")
                    continue
                raise ValueError("Invalid seat")
            new_data.append(new_line)
        return new_data

    def run(self, part):
        data = self.data
        while True:
            new_data = self.one_round(data, part=part)
            if new_data == data:
                break
            data = new_data
        return sum(line.count("#") for line in data)

    def part1(self):
        return self.run(part=1)

    def part2(self):
        return self.run(part=2)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
