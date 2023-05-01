from itertools import product


def getEnhancementString(line) -> str:
    return line.replace("#", "1").replace(".", "0")


def getImage(image):
    return [getEnhancementString(line) for line in image.split("\n")]


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        string, image = open(filename).read().strip().split("\n\n")
        self.ENHANCEMENT = getEnhancementString(string)
        self.image = getImage(image)
        self.answers = list(self.run())

    def generateOutputImage(self, inputImage: list[str], runNr):
        outputImage = []
        for y in range(-1, len(inputImage) + 1):
            row = ""
            for x in range(-1, len(inputImage[0]) + 1):
                s = ""
                for dy, dx in product(range(-1, 2), repeat=2):
                    try:
                        if y + dy < 0 or x + dx < 0:
                            raise IndexError
                        v = inputImage[y + dy][x + dx]
                        s += v
                    except IndexError:
                        # I do not understand why the padding has to be 1 if we are on a odd round number...
                        s += "1" if runNr % 2 == 1 else "0"
                index = int(s, 2)
                value = self.ENHANCEMENT[index]
                row += value
            outputImage.append(row)
        return outputImage

    def run(self):
        image = self.image
        for runNr in range(50):
            image = self.generateOutputImage(image, runNr)
            if runNr == 1:
                yield sum(row.count("1") for row in image)
        yield sum(row.count("1") for row in image)

    def part1(self):
        return self.answers[0]

    def part2(self):
        return self.answers[1]


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
