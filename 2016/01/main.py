from sys import exit

class Taxi1:
    def __init__(self, file):
        self.input = open(file, "r").read()
        self.dir = 0
        self.x = self.y = 0

    def run(self):
        for ins in self.input.split(", "):
            self.turn(ins)

    def turn(self, instruction):
        if "R" in instruction:
            instruction = instruction.replace("R","")
            self.dir += 1
            self.dir %= 4
            self.move(int(instruction))
        elif "L" in instruction:
            instruction = instruction.replace("L","")
            self.dir -= 1
            self.dir %= 4
            self.move(int(instruction))

    def move(self, steps):
        if self.dir == 0:
            self.y -= steps
        elif self.dir == 1:
            self.x += steps
        elif self.dir == 2:
            self.y += steps
        elif self.dir == 3:
            self.x -= steps
        
    def getDistance(self):
        return abs(self.y) + abs(self.x)


class Taxi2:
    def __init__(self, file):
        self.input = open(file, "r").read()
        self.dir = 0
        self.x = self.y = 0
        self.visits = []

    def run(self):
        for ins in self.input.split(", "):
            self.turn(ins)

    def checkDone(self):
        if (self.x, self.y) in self.visits:
            print("Part 2", self.getDistance())
            exit()

    def turn(self, instruction):
        if "R" in instruction:
            instruction = instruction.replace("R","")
            self.dir += 1
            self.dir %= 4
            self.move(int(instruction))
        elif "L" in instruction:
            instruction = instruction.replace("L","")
            self.dir -= 1
            self.dir %= 4
            self.move(int(instruction))

    def move(self, steps):
        if self.dir == 0:
            for _ in range(steps):
                self.y -= 1
                self.checkDone()
                self.visits.append((self.x, self.y))
        elif self.dir == 1:
            for _ in range(steps):
                self.x += 1
                self.checkDone()
                self.visits.append((self.x, self.y))
        elif self.dir == 2:
            for _ in range(steps):
                self.y += 1
                self.checkDone()
                self.visits.append((self.x, self.y))
        elif self.dir == 3:
            for _ in range(steps):
                self.x -= 1
                self.checkDone()
                self.visits.append((self.x, self.y))

    def getDistance(self):
        return abs(self.y) + abs(self.x)


bunny1 = Taxi1("in.txt")
bunny1.run()
print("Part 1:", bunny1.getDistance())

bunny2 = Taxi2("in.txt")
bunny2.run()
