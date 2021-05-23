pieces = [3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]
assert sum(pieces) == (3 * 3 * 3)

class Step:
  def __init__(self, index, pos, direction, fill_state):
    # index - what piece we're on (0 is the first piece...)
    self.index = index

    # pos - where is the "head" of the snake [x, y, z]
    self.pos = pos

    # direction - which way are we going? [1,0,0] is positive x
    self.direction = direction

    # fill_state - what blocks in the cube are already filled?
    self.fill_state = fill_state