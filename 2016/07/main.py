

class answer:
    def __init__(self):
        self.answer = ""
        self.input = open("in.txt").read().splitlines()
        


part1 = answer()
print(part1.input)