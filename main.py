pieces = [3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]
assert sum(pieces) == (3 * 3 * 3)

class Step:
  """A "step" in solving the puzzle, spawning subsequent child steps"""
  def __init__(self, index, pos, direction, fill_state):
    # index - what piece we're on (0 is the first piece...)
    self.index = index

    # pos - position, where is the "head" of the snake (x, y, z)
    self.pos = pos

    # direction - which way are we going? (1,0,0) is positive x
    self.direction = direction

    # fill_state - what blocks in the cube are already filled? A {[coords] => bool} mapping
    self.fill_state = fill_state

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
    for i in piece_len:
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
          Step(self.index+1, final_pos, direction, self.fill_state.copy())
        )

    return next_steps

