data = list(map(int, open("input.txt").read().rstrip().split(",")))
print(min(sum(abs(i - j) for j in data) for i in range(min(data), max(data) + 1)))
