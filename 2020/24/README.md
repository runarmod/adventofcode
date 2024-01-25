# Thoughts on hexgrid

## Three axis

```bash
x = - (to the right)
y = / (up to the right)
z = \ (up to the left)
```

Positive is to the right (with or without up and down as well)

```bash
e:  x += 1
w:  x -= 1
ne: y += 1
sw: y -= 1
se: z += 1
nw: z -= 1
```

## Two axis

```bash
x = - (to the right)
y = / (up to the right)
```

Positive to the right

```bash
e:  x += 1
w:  x -= 1
ne: y += 1
sw: y -= 1
se: x += 1; y -= 1
nw: x -= 1; y += 1
```

CONVERT THREE AXIS TO TWO AXIS:

```bash
(x, y, z) = (x + z, y - z)
```

Examples:

```bash
(1, 1, 1) => (2, 0)
(1, -1, -1) => (0, 0)
(2, 2, 1) => (3, 1)
```

## Conclusion

Might as well use the one with two axis. I think every coordinate is well defined then, in contrast to with three axis, where many (all?) coords have infinite (?) representations:

```bash
three axis: (1, -1, -1) = (-2, 2,  2) = (3, -3, -3) ==> two axis: (0, 0)
three axis: (0,  3 , 0) = ( 1, 2, -1) = (3,  0, -3) ==> two axis: (3, 0)
```
