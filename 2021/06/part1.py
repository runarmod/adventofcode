

class LanternFish():
    def __init__(self, timer):
        self.timer = timer
    
    def grow(self):
        if self.timer == 0:
            self.timer = 6
            lanternFishes.append(LanternFish(8))
        else:
            self.timer -= 1
    
    def getTimer(self):
        return self.timer



lanternFishes = []

def main():
    data = open("input.txt").read().rstrip().split(",")
    # data = open("testinput.txt").read().rstrip().split(",")
    totalDays = 80

    for timer in data:
        lanternFishes.append(LanternFish(int(timer)))

    # print(f"Initial state:\t{','.join(data)}")

    for day in range(totalDays):
        tmpLanternFishes = lanternFishes.copy()
        # Grow every fish in lanternFishe
        for fish in tmpLanternFishes:
            fish.grow()
        # print(f"After {day + 1} day:\t{','.join([str(fish.getTimer()) for fish in tmpLanternFishes])}")
        print(len(lanternFishes))


if __name__ == "__main__":
    main()