import numpy as np

def day5():
    lines: list[list[int]] = [
        [int(x) for x in line.replace(' -> ', ',').split(',')]
        for line in open('input.txt').read().strip().split('\n')
    ]
    def mark(grid: np.ndarray, x0: int, y0: int, x1: int, y1: int):
        dx = np.sign(x1 - x0) 
        dy = np.sign(y1 - y0)
        while x0 != x1+dx or y0 != y1+dy:
            grid[x0, y0] += 1
            x0 += dx
            y0 += dy

    grid = np.zeros((1000, 1000))

    for (x0, y0, x1, y1) in lines:
        if (x0 == x1 or y0 == y1): mark(grid, x0, y0, x1, y1)
    part1 = grid[grid > 1].size

    for (x0, y0, x1, y1) in lines:
        if not (x0 == x1 or y0 == y1): mark(grid, x0, y0, x1, y1)
    part2 = grid[grid > 1].size

    print(f'part1: {part1} / part2: {part2}')

day5()