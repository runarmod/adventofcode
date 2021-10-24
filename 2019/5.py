import requests
from adventofcodeCookie import aoc_cookie

inn = [int(i) for i in requests.get("https://adventofcode.com/2019/day/2/input", cookies=aoc_cookie).text.split(",")]
# inn = [int(i) for i in open("test.txt").read().split(",")]

class IntcodeComputer():
    def __init__(self, noun, verb):
        self.code = inn.copy()
        self.code[1] = noun
        self.code[2] = verb
        self.i = 0

    def one(self):
        self.code[self.code[self.i + 3]] = self.code[self.code[self.i + 1]] + self.code[self.code[self.i + 2]]
        self.i += 4

    def two(self):
        self.code[self.code[self.i + 3]] = self.code[self.code[self.i + 1]] * self.code[self.code[self.i + 2]]
        self.i += 4
    
    def three(self):
        
    
    def run(self):
        while True:
            if self.code[self.i] == 99:
                break
            elif self.code[self.i] == 1:
                self.one()
            elif self.code[self.i] == 2:
                self.two()
            else:
                print("Encountered unknown command", self.code[self.i], "i is", self.i)
