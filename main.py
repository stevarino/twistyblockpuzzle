pieces = [3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]
assert sum(pieces) == (3 * 3 * 3)

# Build a 3x3x3 array filled with zeros
initial_fill_state = [[[0] * 3] * 3] * 3

class Step:
  """A "step" in solving the puzzle, spawning subsequent child steps"""
  def __init__(self, index, pos, direction, fill_state):
    # index - what piece we're on (0 is the first piece...)
    self.index = index

    # pos - position, where is the "head" of the snake [x, y, z]
    self.pos = pos

    # direction - which way are we going? [1,0,0] is positive x
    self.direction = direction

    # fill_state - what blocks in the cube are already filled?
    self.fill_state = fill_state

  def next(self):
    """Returns the four next logical steps, or zero steps if currently illegal"""
    # first, am i legal? Do I exit the bounds of 3x3x3, or do i intersect an
    # already filled block?

    piece_len = pieces[self.index]
    final_pos = [self.pos[i] + (self.direction[i] * piece_len) for i in range(3)]
    
    # the only values should be 0,1,2
    if not all(0 <= val <= 2 for val in final_pos):
      return []
    
    # next, lets update fill_state, checking that its not already filled
    for i in piece_len:
      self.pos = [self.pos[i] + self.direction[i] for i in range(3)]
      # check that the currnt value is 0
      focus = self.fill_state
      for val in self.pos[0:-1]:  # all but the last last dimension (z)
        focus = focus[val]
      if focus[self.pos[-1]] == 1:  # now we read the last dimension...
        # we've focused on a filled square... we're in an illegal state
        return []
      # mark the box as filled
      focus[self.pos[-1]] = 1
    
