# 2022 - day 22

I do not usually write any additional information about my solutions, but this day I have spent waaay to much time on, and I do not think my solution is possible to understand at all without a little information.

I first started doing this puzzle on descember 22nd, and I managed to do part 1 relatively easily. Part 2 however, I couldn't get for the life of me. I knew early on that I did notcare to make my solution general, since I genuinely had no clue how to do so. Therefore I made my first attempt extremely redundant. I calculated the new coordinate in an extremely irritating way. For example if new coordinate was (100, 48), I set it to something like (202, 200) instead (obviously not correct example, but that doesn't matter).

Now I've created a somewhat better solution (really low code quality still though ._. ), which works on test-inputs, and other people's input without waaay too much effort. To use, copy each square of the cube into their own file. Let the start-face be "top", and the other faces based on that face. Then change the np.rot90 rotation argument, so that the front, left, right and back all have their top row (index 0) upwards (the side where the top-face should be). Top-face should have its top-row towards the back, and the bottom-row towards the front. The bottom-face should have its top-row towards the front, and the bottom-row towards the back.

Now the code should be ready to run. Just also make sure to change the match-case in the end so it works for your input (you have to figure out how to change the x/y-coords/direction to be back in the original format).

You can uncomment a line to see with 3d-matplotlib where your path goes. Really good for debugging with test-cases. Possible to use with real input as well, but reeeally slow.
