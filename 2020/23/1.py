inn = str(538914762).split()

current_cup_index = 0

for turn in range(100):
    pick_up = [inn[(current_cup_index + 1) % len(inn)], inn[(current_cup_index + 2) % len(inn)], inn[(current_cup_index + 3) % len(inn)]]

    destination = (inn[current_cup_index] - 1) % len(inn)
    while destination in pick_up:
        destination = (inn[current_cup_index] - 1) % len(inn)

    destination_index, pick_up_index = inn.index(destination), inn.index(pick_up)
    inn[]