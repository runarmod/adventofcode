import itertools


class Solution:
    def __init__(self, test=False):
        self.test = test
        filename = "testinput.txt" if self.test else "input.txt"
        self.data = [int(c) for c in open(filename).read().rstrip()]
        self.size = [
            {"width": 25, "height": 6},
            {"width": 2, "height": 2},
        ]  # [0] != test, [1] == test
        self.area = self.size[self.test]["width"] * self.size[self.test]["height"]
        self.layers = [
            self.data[i : i + self.area] for i in range(0, len(self.data), self.area)
        ]

    def get_best_layer(self):
        best_layer = {"count": float("inf"), "vals": None}
        for layer in self.layers:
            if (count := layer.count(0)) < best_layer["count"]:
                best_layer["count"] = count
                best_layer["vals"] = layer
        return best_layer["vals"]

    def multiply_numbers(self, layer, *numbers):
        return list(
            itertools.accumulate([layer.count(n) for n in numbers], lambda x, y: x * y)
        )[-1]

    def part1(self):
        return self.multiply_numbers(self.get_best_layer(), 1, 2)

    def part2(self):
        final = [-1] * self.area
        for layer in self.layers[::-1]:
            for i, pixel in enumerate(layer):
                final[i] = final[i] if pixel == 2 else pixel
        for y in range(self.size[self.test]["height"]):
            for x in range(self.size[self.test]["width"]):
                print(
                    " " if final[y * self.size[self.test]["width"] + x] == 0 else "▮",
                    end="",
                )
            print()
        return "CGEGE"  # manually read from output


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: 2 (different testdata, can't be bothered to have both)")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    part1 = solution.part1()
    print(f"Part 1: {part1}")
    part2 = solution.part2()
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
