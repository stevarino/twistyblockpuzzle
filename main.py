"""
Twisty Block Puzzle Solver

So I have this block puzzle toy that I got for Christmas which I pulled apart and
never could put back together: https://i.imgur.com/qXTnaJF.jpeg

It's a string of cubes, some are in line with each other but others bend at right
angles. The idea is that it should fold together into a 3x3x3 cube. I've tried to
reassemble it for hours but I guess I'm not smart enough? Python to the rescue!!!

First step is to lay it out flat so we can see its shape, allowing us to count all
the lengths of each "elbow": https://i.imgur.com/FZmZupl.jpeg

So we can see that (reading fro the left) it goes up 3, then right 1, then up 1, 
right 2, etc. The actual directions don't matter, just that there's a turn after
"n" blocks (n being some number). This allows us to "map" the toy into a data
structure: [3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]

Next thing to realize is that each bend in the toy has four options. For instance,
that first bend can either go left, right, up, or down. Every bend opens up four
possible solutions, and after all 16 bends we end up with about 4.3 BILLION
possibilities. However, not all soultions are valid, as in the real world two blocks
cannot occupy the same unit of space and we know the final solution will have all
blocks in a 3x3x3 area.

So imagine a tree with four branches at each split. By figuring out which branch is
illegal (impossible or outside the 3x3x3 area) we prune them before exploring them
fully. Then we continue searching through the branch possibilities that look valid.

Turns out there are 8 total solutions for this puzzle, and by eliminating the invalid
steps as early as possible we end up with 845 possibilities that we need to explore.

The final output of this program simply displays the directions I need to snake the
blocks for each leg. I chose to use "X Y x Z Y z X Z y x Y z Y Z y X Y X" with capital
letters representing positive direction and lowercase negative direction (X=right,
x=left, Y=up, y=down, Z=back, z=forward). Thus the program outputs a "human program"
for me to follow and get what I want.

Final solution: https://i.imgur.com/nVxnx3n.jpeg TADA!

(Used)
"""

pieces = [3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]

assert sum(pieces) == (3 * 3 * 3)  # Double check that we have enough to make a cube

class Step:
  """A "step" in solving the puzzle, spawning subsequent child steps"""
  def __init__(self, index=0, pos=None, direction=None, fill_state=None, prev_step=None):
    # index - what piece we're on (0 is the first piece...)
    self.index = index

    # pos - position, where is the "head" of the snake (x, y, z)
    # NOTE: starting at -1 x as we are going to be placing the first block
    # in the (x) direction.
    self.pos = pos or (-1, 0, 0)

    # direction - which way are we going? (1,0,0) is pos x, (0,-1,0) is neg y
    self.direction = direction or (1, 0, 0)

    # fill_state - what blocks in the cube are already filled? A {[coords] => bool} mapping
    self.fill_state = fill_state or {}

    # prev_step - a reference to the step that spawned this step
    self.prev_step = prev_step

  def next(self):
    """Returns the four next logical steps, or zero steps if currently illegal"""
    # first, am i legal? Do I exit the bounds of 3x3x3, or do i intersect an
    # already filled block?

    piece_len = pieces[self.index]
    final_pos = tuple(self.pos[i] + (self.direction[i] * piece_len) for i in range(3))
    
    # the only values should be 0,1,2
    if not all(0 <= val <= 2 for val in final_pos):
      return []
    
    # next, lets update fill_state, checking that its not already filled
    for i in range(piece_len):
      self.pos = tuple(self.pos[i] + self.direction[i] for i in range(3))
      # check that the currnt value is 0
      if self.fill_state.get(self.pos):
        return []
      # mark the box as filled
      self.fill_state[self.pos] = True
    
    # And if we made it this far, we know now that the Step is valid

    # sanity check that we're where we should be
    assert final_pos == self.pos

    # Next we need to find the four directions we can turn
    next_steps = []
    for i in range(len(self.direction)):
      # if we're moving in this direction (pos or neg), we can't turn that way
      if self.direction[i] != 0:
        continue
      for posneg in [1, -1]:
        direction = [0, 0, 0]
        direction[i] = posneg
        next_steps.append(
          Step(self.index+1, final_pos, direction, self.fill_state.copy(), self)
        )

    return next_steps

  def __str__(self):
    """Returns string rep of directions (capital X is pos x, lowercase x is neg x)"""
    prev_directions = ""
    if self.prev_step:
      prev_directions = str(self.prev_step) + ' '
    direction = '?'
    for scale, name in zip(self.direction, 'xyz'):
      if scale == 0:
        continue
      if scale == 1:
        direction = name.upper()
      else:
        direction = name
    return prev_directions + direction

def main():
  steps = [Step()]
  total_steps = 0
  while steps:
    step = steps.pop(0)
    if step.index == len(pieces):
      print(step)
    else:
      steps.extend(step.next())
    total_steps += 1
  print("Examined {} steps".format(total_steps))

if __name__ == '__main__':
  main()
