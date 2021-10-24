puzzle_input = "1321131112"

def count_number(next_index):
    number = puzzle_input[next_index]
    i = next_index
    count = 0
    while i < len(puzzle_input) and puzzle_input[i] == number:
        i += 1
        count += 1
    next_index += count

    return count, number, next_index

def calculate(times):
    global puzzle_input
    for turn in range(times):
        new_number, next_index = "", 0
        while next_index < len(puzzle_input):
            count, number, next_index = count_number(next_index)
            new_number += str(count) + number
        puzzle_input = new_number
    return len(puzzle_input)

print("Part 1:", calculate(40))
print("Part 2:", calculate(50))

