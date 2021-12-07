fish_count = [0] * 9

for fish in open("input.txt").read().rstrip().split(","):
    fish_count[int(fish)] += 1

for _ in range(1000000):
    fish_count.append(fish_count.pop(0))
    fish_count[6] += fish_count[8]
print(sum(fish_count))