print(
    "\n".join(
        map(
            str,
            (
                lambda data: (
                    (lengths := sum(len(d) for d in data))
                    - sum(len(eval(d)) for d in data),
                    sum(
                        (lambda s: len(s) + s.count("\\") + s.count('"') + 2)(s)
                        for s in data
                    )
                    - lengths,
                )
            )(open("input.txt").read().strip().split("\n")),
        )
    )
)
