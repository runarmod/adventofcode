import heapq
import time

# from pprint import pprint


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [
            list(map(int, list(line)))
            for line in open(filename).read().rstrip().split("\n")
        ]

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)

    def run(self, part):
        q = []
        # Include the list in the queue if you want to print the route
        heapq.heappush(
            q,
            (
                0,
                0,
                0,
                -1,
                -1,
                # []
            ),
        )  # distance, x, y, dir, same_direction, route
        visited = set()
        while q:
            (
                dist,
                x,
                y,
                _dir,
                same_direction,
                # route,
            ) = heapq.heappop(q)

            if x == len(self.data[0]) - 1 and y == len(self.data) - 1:
                # self.print_route(route)
                return dist

            if (x, y, _dir, same_direction) in visited:
                continue

            visited.add((x, y, _dir, same_direction))

            for new_dir, (dx, dy) in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
                # Can't turn back
                if (new_dir + 2) % 4 == _dir:
                    continue

                new_same_distance = same_direction + 1 if new_dir == _dir else 1

                valid = (
                    new_same_distance <= 3
                    if part == 1
                    else new_same_distance <= 10
                    and (new_dir == _dir or same_direction >= 4 or same_direction == -1)
                )

                if (
                    0 <= x + dx < len(self.data[0])
                    and 0 <= y + dy < len(self.data)
                    and valid
                ):
                    heapq.heappush(
                        q,
                        (
                            dist + self.data[y + dy][x + dx],
                            x + dx,
                            y + dy,
                            new_dir,
                            new_same_distance,
                            # route + [(x + dx, y + dy)],
                        ),
                    )
        return None

    def print_route(self, route):
        green = "\033[92m"
        end = "\033[0m"
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if (x, y) in route:
                    print(f"{green}O{end}", end="")
                else:
                    print(self.data[y][x], end="")
            print()


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 102 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 94 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
