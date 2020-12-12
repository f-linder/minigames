class lBlock():
    def __init__(self):
        self.state = 0
        self.num_states = 4
        # facing means straight line to side
        # state 0 -> facing up
        # state 1 -> facing left
        # state 2 -> facing down
        # state 3 -> facing right
        self.pos = [[3, -1], [4, -1], [5, -1], [3, 0]]

    def change_state(self, array):
        if self.state == 0 and self.to_left_possible(array):
            self.to_left()
            self.state += 1
        elif self.state == 1 and self.to_down_possible(array):
            self.to_down()
            self.state += 1
        elif self.state == 2 and self.to_right_possible(array):
            self.to_right()
            self.state += 1
        elif self.state == 3 and self.to_up_possible(array):
            self.to_up()
            self.state += 1
        self.state %= self.num_states

    def to_left_possible(self, array):
        # reference is the middle peace
        x, y = self.pos[1]
        if array[x][y + 1] != -1 or array[x + 1][y + 1] != -1:
            return False
        # checking above
        elif y - 1 < 0:
            return True
        elif array[x][y - 1] != - 1:
            return False
        return True

    def to_left(self):
        # reference is the middle peace
        x, y = self.pos[1]
        # left line, top to bottom, peace to the right
        self.pos = [[x, y - 1], [x, y], [x, y + 1], [x + 1, y + 1]]

    def to_down_possible(self, array):
        # reference is the middle peace
        x, y = self.pos[1]
        # in bounds left and right
        if x - 1 < 0 or x + 1 >= 10:
            return False
        # if in bounds -> are there blocks?
        elif array[x + 1][y] != -1 or array[x - 1][y] != -1:
            return False
        # block to the top right
        elif y - 1 < 0:
            return True
        elif array[x + 1][y - 1] != -1:
            return False
        return True

    def to_down(self):
        # reference is the middle peace
        x, y = self.pos[1]
        self.pos = [[x - 1, y], [x, y], [x + 1, y], [x + 1, y - 1]]

    def to_right_possible(self, array):
        # reference block is the one in the middle
        x, y = self.pos[1]
        # left and right bound not interesting
        if y + 1 >= 20:
            return False
        elif array[x][y + 1] != -1:
            return False
        elif y - 1 < 0:
            return True
        elif array[x][y - 1] != -1 or array[x - 1][y - 1] != -1:
            return False
        return True
         
    def to_right(self):
        x, y = self.pos[1]
        self.pos = [[x, y - 1], [x, y], [x, y + 1], [x - 1, y - 1]]

    def to_up_possible(self, array):
        x, y = self.pos[0]
        if x + 1 >= 10:
            return False
        elif array[x - 1][y] != -1 or array[x + 1][y] != -1:
            return False
        elif array[x - 1][y + 1] != -1:
            return False
        return True

    def to_up(self):
        x, y = self.pos[0]
        self.pos = [[x - 1, y], [x, y], [x + 1, y], [x - 1, y + 1]]

