from copy import deepcopy
import itertools
import re
from collections import deque


def parseLine(line):
    # Ugly :((
    return [
        re.sub(r" (microchip|generator)", r"", val)
        for val in re.split(
            r"(?:, a )|(?:,? and a )",
            re.sub(r"The \w+ floor contains (a )?(nothing relevant)?", r"", line[:-1]),
        )
        if len(val) > 0
    ]


# Negatives = chip
# Positive = generator
def parseData(data):
    i = 1
    chipDict = {}
    out = []
    for row in data:
        rowSet = set()
        for item in row:
            itemClean = item.split("-")[0] if "-" in item else item
            if itemClean in chipDict:
                rowSet.add(-chipDict[itemClean])
                continue

            if "-" in item:
                rowSet.add(-i)
                chipDict[itemClean] = -i
            else:
                rowSet.add(i)
                chipDict[itemClean] = i
            i += 1
        out.append(rowSet)
    return out


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        data = map(parseLine, open(filename).read().rstrip().split("\n"))
        self.data = parseData(data)

    def state_equivalent(self, state1, state2):
        """
        Two states does not have to be equal to be equivalent
        Example:
        [{1}, {-1}, {2, -2}]
        can be considered the same as
        [{2}, {-2}, {1, -1}]
        """
        floors1, elevator1 = state1
        floors2, elevator2 = state2
        if elevator1 != elevator2:
            return False
        if any(len(floors1[i]) != len(floors2[i]) for i in range(4)):
            return False
        max_i = max(max(floor) for floor in floors1 if len(floor) > 0)

        floors = {0: floors1, 1: floors2}
        pair_floors = {0: set(), 1: set()}
        for id in range(2):
            for i in range(1, max_i + 1):
                positive = None
                negative = None
                for floor_nr in range(len(floors[id])):
                    if i in floors[id][floor_nr]:
                        if negative is None:
                            positive = floor_nr
                        else:
                            pair_floors[id].add((negative, floor_nr))
                            break
                    if -i in floors[id][floor_nr]:
                        if positive is None:
                            negative = floor_nr
                        else:
                            pair_floors[id].add((floor_nr, positive))
                            break
        return pair_floors[0] == pair_floors[1]

    def valid_floor(self, floor):
        if len(floor) <= 1:
            return True
        return not any(
            item1 < 0 and -item1 not in floor and any(item2 > 0 for item2 in floor)
            for item1 in floor
        )

    def valid_move(self, new_state, elevator, items, direction):
        if elevator + direction < 0 or elevator + direction > 3:
            return False

        return (
            all(self.valid_floor(floor) for floor in new_state)
            if self.valid_floor(items)
            else False
        )

    def move(self, state, elevator, items, direction):
        new_state = deepcopy(state)
        new_state[elevator] = new_state[elevator] - set(items)
        new_state[elevator + direction] = new_state[elevator + direction] | set(items)
        return new_state

    def create_queues(self, state, elevator, steps):
        # idexes:
        # outer = direction (up = 1, down = -1 => 0)
        # inner = number of items (minus 1)
        qs = [[deque(), deque()], [deque(), deque()]]

        # Itertools <3 <3
        for items, direction in itertools.product(
            itertools.chain(
                itertools.combinations(state[elevator], 2),
                itertools.combinations(state[elevator], 1),
            ),
            (-1, 1),
        ):
            new_elevator = elevator + direction
            if new_elevator < 0 or new_elevator > 3:
                continue
            new_state = self.move(state, elevator, items, direction)
            if self.valid_move(new_state, elevator, items, direction):
                qs[(direction + 1) // 2][len(items) - 1].append(
                    (new_state, new_elevator, steps + 1)
                )
        return qs[1][0], qs[1][1], qs[0][0], qs[0][1]

    def bfs(self):
        q = deque()
        q.append((deepcopy(self.data[:]), 0, 0))
        visited = set()
        while q:
            state, elevator, steps = q.popleft()

            if all(len(floor) == 0 for floor in state[:-1]):
                return steps

            frozenFloors = tuple(frozenset(floor) for floor in state)
            
            # O(1) lookup
            if (frozenFloors, elevator) in visited:
                continue

            # May still be equivalent even if not equal
            if any(self.state_equivalent((frozenFloors, elevator), state2) for state2 in visited):
                continue

            visited.add((frozenFloors, elevator))
            self.extend_q(q, *self.create_queues(state, elevator, steps))

        return None

    def extend_q(self, q, up1item, up2items, down1item, down2items):
        q.extend(up2items)
        if len(up2items) == 0:
            q.extend(up1item)
        q.extend(down1item)
        if len(down1item) == 0:
            q.extend(down2items)

    def part1(self):
        return self.bfs()

    def part2(self):
        # new_items = ["elerium" "elerium-compatible", "dilithium", "dilithium-compatible"]
        max_id = max(max(row) for row in self.data if len(row) > 0)
        add = tuple(range(max_id + 1, max_id + 1 + 2))
        self.data[0] = self.data[0] | {*add, *map(lambda x: -x, add)}
        return self.bfs()


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
