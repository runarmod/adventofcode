(
    lambda data: [
        print(
            f"Part {part}:",
            sum(
                ID
                for r in (
                    range(f, t + 1)
                    for f, t in __import__("itertools").batched(
                        map(int, __import__("re").findall(r"\d+", data)), 2
                    )
                )
                for ID in r
                if __import__("re").match(
                    r"^(.+)\1+$" if part == 2 else r"^(.+)\1$", str(ID)
                )
                is not None
            ),
        )
        for part in (1, 2)
    ]
)(input())
