import re


def parseLine(line):
    return tuple(map(int, re.findall(r"-?\d+", line)))


class Solution:
    def __init__(self, test=False):
        filename = "testinput.txt" if test else "input.txt"
        self.data = [parseLine(line) for line in open(filename).read().rstrip().split("\n")]

    def manhattan(self, coords):
        return sum(abs(coord) for coord in coords)

    def part1(self):
        return self.data.index(
            min(
                self.data,
                key=lambda x: (
                    self.manhattan(x[-3:]),
                    self.manhattan(x[3:-3]),
                    self.manhattan(x[:3]),
                ),
            )
        )

    def update_thing(self, pos, vel, acc):
        new_vel = tuple(v + a for v, a in zip(vel, acc))
        new_pos = tuple(p + v for p, v in zip(pos, new_vel))
        return new_pos, new_vel, acc

    def part2(self):
        particles = {settings[:3]: settings for settings in self.data}
        # For my data, 100 iterations was enough to get a stable number of particles
        # However, this is not guaranteed to be true for all data
        # First time i tried this, i used 50_000 iterations, to be sure it was enough
        for _ in range(100):
            new_particles = {}
            delete = set()
            for _, particle in particles.items():
                pos, vel, acc = particle[:3], particle[3:-3], particle[-3:]

                new_pos, new_vel, new_acc = self.update_thing(pos, vel, acc)
                new_particle = tuple((*new_pos, *new_vel, *new_acc))

                if new_pos in new_particles:
                    delete.add(new_pos)
                else:
                    new_particles[new_pos] = new_particle

            for pos in delete:
                del new_particles[pos]
            particles = new_particles
        return len(particles)


def main():
    test = Solution(test=True)
    print(f"(TEST) Part 1: {test.part1()}")
    print(f"(TEST) Part 2: {test.part2()}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")


if __name__ == "__main__":
    main()
