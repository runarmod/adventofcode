monkeys = {
    monkey: actions.split(" ")
    for line in open("input.txt").read().splitlines()
    for monkey, actions in [line.split(": ")]
}
run = (
    lambda monkey: monkeys[monkey][0]
    if len(monkeys[monkey]) == 1
    else f"({run(monkeys[monkey][0])}{monkeys[monkey][1]}{run(monkeys[monkey][2])})"
)
print(int(eval(run("root"))))


monkeys = {
    monkey: ["x"]
    if monkey == "humn"
    else actions.split(" ")
    if monkey != "root"
    else [actions.split(" ")[0], "-", actions.split(" ")[2]]
    for line in open("input.txt").read().splitlines()
    for monkey, actions in [line.split(": ")]
}
run = (
    lambda monkey: monkeys[monkey][0]
    if len(monkeys[monkey]) == 1
    else f"({run(monkeys[monkey][0])}{monkeys[monkey][1]}{run(monkeys[monkey][2])})"
)
print(__import__("sympy").solve(run("root"))[0])
