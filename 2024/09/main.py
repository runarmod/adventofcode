from collections import deque
import re
import time

from aoc_utils_runarmod import get_data


def parseNumbers(line):
    return tuple(map(int, re.findall(r"\d", line)))


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = (
            get_data(2024, 9) if not self.test else open("testinput.txt").read()
        ).rstrip()

        self.data = parseNumbers(data)

    def run(self, part: int):
        files, space, result_list = [], [], []

        file_id = 0
        position = 0
        for i in range(len(self.data)):
            if i % 2 == 0:
                # For part 1, we look at files per block, for part 2 we have to keep entire files together
                files.extend(
                    [(file_id, position + j, 1) for j in range(self.data[i])]
                    if part == 1
                    else [(file_id, position, self.data[i])]
                )
                result_list.extend([file_id] * self.data[i])
                file_id += 1
            else:
                space.append((position, self.data[i]))
                result_list.extend([-1] * self.data[i])
            position += self.data[i]

        # Only try once per file
        for file_id, file_pos, file_size in reversed(files):
            if (
                space[0][0] > file_pos
            ):  # No more files can be moved to the left if the first space is to the right of the file
                break
            # Find first space that fits the file
            for space_i, (space_pos, space_size) in enumerate(space):
                if space_pos >= file_pos:  # We should not move files further back
                    break
                if (
                    space_size < file_size
                ):  # We have to find a space that fits the entire file
                    continue
                # Swap the file and space
                result_list[space_pos : space_pos + file_size] = [file_id] * file_size
                result_list[file_pos : file_pos + file_size] = [-1] * file_size

                # Update space, and optionally remove the (empty) space
                space[space_i] = (space_pos + file_size, space_size - file_size)
                if space_size == file_size:
                    del space[space_i]
                break  # We have found a space for the file

        return sum(i * num for i, num in enumerate(result_list) if num != -1)

    def part1(self):
        return self.run(1)

    def part2(self):
        return self.run(2)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1928 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 2858 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
