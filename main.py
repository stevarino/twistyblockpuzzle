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

def main(breadth_first=True):
  steps = [Step()]
  total_steps = 0
  # which end of the steps to pop from? 0 = beginning and breadth first, -1 is end
  # and therefore depth first
  pop_index = 0 if breadth_first else -1
  while steps:
    step = steps.pop(pop_index)
    if step.index == len(pieces):
      print(total_steps, ':', step)
    else:
      steps.extend(step.next())
    total_steps += 1
  print("Examined {} steps".format(total_steps))

if __name__ == '__main__':
  print("Breadth first search:")
  main(breadth_first=True)
  print("\nDepth first search:")
  main(breadth_first=False)
