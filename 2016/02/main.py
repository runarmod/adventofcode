
class Lock1:
    def __init__(self, file):
        self.keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.x = 1
        self.y = 1
        self.input = open(file).read().splitlines()
        self.code = ""

    def find_code(self):
        for line in self.input:
            for move in line:
                if move == "U":
                    self.y = max(0, self.y - 1)
                elif move == "L":
                    self.x = max(0, self.x - 1)
                elif move == "D":
                    self.y = min(2, self.y + 1)
                elif move == "R":
                    self.x = min(2, self.x + 1)

            self.code += str(self.keypad[self.y][self.x])

    def print_code(self):
        print(self.code)


class Lock2:
    def __init__(self, file):
        self.keypad = [[0, 0, 1, 0, 0], [0, 2, 3, 4, 0], [5, 6, 7, 8, 9], [0, "A", "B", "C", 0], [0, 0, "D", 0, 0]]
        self.x = 0
        self.y = 2
        self.input = open(file).read().splitlines()
        self.code = ""

    def find_code(self):
        for line in self.input:
            for move in line:
                if move == "U":
                    if self.topleft() and self.topleft():
                        self.y = max(0, self.y - 1)
                elif move == "L":
                    if self.topleft() and self.bottomleft():
                        self.x = max(0, self.x - 1)
                elif move == "D":
                    if self.bottomleft() and self.bottomright():
                        self.y = min(4, self.y + 1)
                elif move == "R":
                    if self.topright() and self.bottomright():
                        self.x = min(4, self.x + 1)
            print(self.x, self.y)
            self.code += str(self.keypad[self.y][self.x])

    def topleft(self):
        return self.y + self.x > 2
    
    def topright(self):
        return self.x - self.y < 2
    
    def bottomleft(self):
        return self.y - self.x < 2
    
    def bottomright(self):
        return self.x + self.y < 6
    

    def print_code(self):
        print(self.code)


# part1 = Lock1("in.txt")
# part1.find_code()
# part1.print_code()

part2 = Lock2("in.txt")
part2.find_code()
part2.print_code()
