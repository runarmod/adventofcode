import itertools
import re
import time
from collections import defaultdict


def parseData(lines):
    flows: dict[str, int] = {}
    roads: dict[str, set[str]] = {}
    for line in lines:
        valve, *valves = re.findall(r"([A-Z]{2})", line)
        flow = re.findall(r"(\d+)", line)[0]
        flows[valve] = flow
        roads[valve] = set(valves)
    return flows, roads


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        flows, roads = parseData(open(filename).read().rstrip().split("\n"))

        self.distances = self.floyd_warshall(roads)
        self.flows = {valve: int(flow) for valve, flow in flows.items() if flow != "0"}
        self.valve_masks = {valve: 1 << i for i, valve in enumerate(self.flows)}

    def floyd_warshall(self, roads: dict[str, set[str]]):
        dist: defaultdict[str, defaultdict[str, int]] = defaultdict(
            lambda: defaultdict(lambda: 1000)
        )
        for valve, valves in roads.items():
            for v in valves:
                dist[valve][v] = 1

        for k, i, j in itertools.product(roads.keys(), repeat=3):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        return dist

    def new_dfs(
        self,
        valve: str,
        state_bitmask: int,
        pressure: int,
        remaining_minutes: int,
        visited_flow: dict[int, int],
    ) -> dict[int, int]:
        visited_flow[state_bitmask] = max(visited_flow.get(state_bitmask, 0), pressure)

        for valve2, flow in self.flows.items():
            if self.valve_masks[valve2] & state_bitmask:
                continue

            new_remaining_minutes = remaining_minutes - self.distances[valve][valve2] - 1
            if new_remaining_minutes <= 0:
                continue

            new_valves_on = state_bitmask | self.valve_masks[valve2]
            new_pressure = pressure + flow * new_remaining_minutes

            self.new_dfs(
                valve2,
                new_valves_on,
                new_pressure,
                new_remaining_minutes,
                visited_flow,
            )

        return visited_flow

    def part1(self):
        return max(self.new_dfs("AA", 0, 0, 30, {}).values())

    def part2(self):
        finished_states = self.new_dfs("AA", 0, 0, 26, {})
        return max(
            flow1 + flow2
            for visitedmask1, flow1 in finished_states.items()
            for visitedmask2, flow2 in finished_states.items()
            if not visitedmask1 & visitedmask2  # no overlap
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
