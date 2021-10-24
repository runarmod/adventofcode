import requests
from adventofcodeCookie import aoc_cookie
from tqdm import trange

lines = [line.split(",") for line in requests.get("https://adventofcode.com/2019/day/3/input", cookies=aoc_cookie).text.splitlines()]


######################### PART 1:
# points = [[], []]
# meetingpoints = []
# for i, line in enumerate(lines):
#     x = 0
#     y = 0
#     for instruction in line:
#         if instruction.startswith("U"):
#             for _ in range(int(instruction[1:])):
#                 y -= 1
#                 points[i].append((x, y))
#         elif instruction.startswith("L"):
#             for _ in range(int(instruction[1:])):
#                 x -= 1
#                 points[i].append((x, y))
#         elif instruction.startswith("D"):
#             for _ in range(int(instruction[1:])):
#                 y += 1
#                 points[i].append((x, y))
#         elif instruction.startswith("R"):
#             for _ in range(int(instruction[1:])):
#                 x += 1
#                 points[i].append((x, y))
        
# for i in trange(len(points[0])):
#     coord = points[0][i]
#     if coord in points[1]:
#         meetingpoints.append(coord)

# print(meetingpoints)


# for i in range(len(meetingpoints)):
#     meetingpoints[i] = abs(meetingpoints[i][0]) + abs(meetingpoints[i][1])

# print(sorted(meetingpoints))



######################### PART 2:

meetingpoints = [(140, -1763), (140, -2328), (-91, -2578), (-159, -1485), (-157, -1027), (-37, -1027), (-37, -1695), (140, -2520), (-37, -1055), (-157, -1055), (-297, -936), (-297, -801), (-749, -801), (-981, -828), (-1003, -828), (-560, 2681), (-560, 2917), (64, 3217), (128, 3101), (128, 2948), (128, 2895), (128, 2856), (38, 2323), (-14, 2323), (-26, 2296), (-26, 2286), (-14, 2131), (38, 2131), (172, 2131), (617, 2356), (-14, 2356), (-144, 2325), (-144, 2296), (-144, 2286), (155, 1930), (479, 1968), (155, 1990), (38, 1990), (-244, 2286), (-244, 2296), (-244, 2325), (-244, 2895), (-244, 2917), (570, 3101), (64, 3180), (-381, 3275), (889, 3434)]
meetingpoints = [list(elem) for elem in meetingpoints]

lengthToPoints = [0]* len(meetingpoints)
print(lengthToPoints)
for i, line in enumerate(lines):
    coord = [0, 0]
    length = 0
    for instruction in line:
        if instruction.startswith("U"):
            for _ in range(int(instruction[1:])):
                coord[1] -= 1
                length += 1
                if coord in meetingpoints:
                    lengthToPoints[meetingpoints.index(coord)] += length
        elif instruction.startswith("L"):
            for _ in range(int(instruction[1:])):
                coord[0] -= 1
                length += 1
                if coord in meetingpoints:
                    lengthToPoints[meetingpoints.index(coord)] += length
        elif instruction.startswith("D"):
            for _ in range(int(instruction[1:])):
                coord[1] += 1
                length += 1
                if coord in meetingpoints:
                    lengthToPoints[meetingpoints.index(coord)] += length
        elif instruction.startswith("R"):
            for _ in range(int(instruction[1:])):
                coord[0] += 1
                length += 1
                if coord in meetingpoints:
                    lengthToPoints[meetingpoints.index(coord)] += length
print(sorted(lengthToPoints))