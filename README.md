Twisty Block Puzzle Solver

So I have this block puzzle toy that I got for Christmas which I pulled apart and
never could put back together: https://i.imgur.com/qXTnaJF.jpeg

It's a string of cubes, some are in line with each other but others bend at right
angles. The idea is that it should fold together into a 3x3x3 cube. I've tried to
reassemble it for hours but I guess I'm not smart enough? Python to the rescue!!!

First step is to lay it out flat so we can see its shape, allowing us to count all
the lengths of each "elbow": https://i.imgur.com/FZmZupl.jpeg

So we can see that (reading from the left) it goes up 3, then right 1, then up 1, 
right 2, etc. The actual directions don't matter, just that there's a turn after
"n" blocks. This allows us to "map" the toy into a data structure: 
[3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]

Next thing to realize is that each bend in the toy has four options. For instance,
that first bend can either go left, right, up, or down. Every bend opens up four
possible solutions, and after all 16 bends we end up with about 4.3 BILLION
possibilities. However, not all soultions are valid, as in the real world two blocks
cannot occupy the same unit of space and we know the final solution will have all
blocks in a 3x3x3 area.

So imagine a tree with four branches at each split. By figuring out which branch is
illegal (impossible or outside the 3x3x3 area) we prune them before exploring them
fully. Then we continue searching through the branch possibilities that look valid.

So after applying these rules and eliminating illegal possibliites as early as
possible, we end up with 845 intermediate steps that we need to explore, with a 
total of 8 solutions for this puzzle.I chose to use "X Y x Z Y z X Z y x Y z Y Z y X
Y X" (X=right, x=left, Y=up, y=down, Z=back, z=forward) and it totally worked:
https://i.imgur.com/nVxnx3n.jpeg

Thus the program outputs a "human program" for me to follow and get what I want.

This program was written to be followed along with in a hopefully straightfoward
manner. It could absolutely be written in different methods with different
algorithms but I chose a simple breadth-first search as that seemed relatively
simple and efficient. As I was writing it I considered expansions to this program.
What if we tried to find solutions that were not a 3x3x3 cube? How about a 4x4x4
cube? Or a 8x5x22 box? We could also apply this algorithm to a 2d flat shape (3x3
for instance, with a possible toy being [3,2,2,1,1]). Or if we really want to hurt
or brains, convert this program into a 4d cube solver where each bend now allows
six possibilities. This may sound difficult, but the algorithm can actually be
easily adapted.

Total Output:

```
X Y x Z Y z X Z y x Y z Y Z y X Y X
X Y x Z Y z X Z y x Y z Y Z y X Y x
X Y x Z Y z X Z y x Y z Y Z y X Y Z
X Y x Z Y z X Z y x Y z Y Z y X Y z
X Z x Y Z y X Y z x Z y Z Y z X Z X
X Z x Y Z y X Y z x Z y Z Y z X Z x
X Z x Y Z y X Y z x Z y Z Y z X Z Y
X Z x Y Z y X Y z x Z y Z Y z X Z y
Examined 845 steps
```