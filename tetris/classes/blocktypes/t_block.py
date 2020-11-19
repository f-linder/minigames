class tBlock():
    def __init__(self):
        self.state = 0
        self.num_states = 4
        # state 0 -> facing down
        # state 1 -> facing right
        # state 2 -> facing up
        # state 3 -> facing left
        self.pos = [[3, -1], [4, -1], [5, -1], [4, 0]]

    def change_state(self, array):
        if self.state == 0 and self.to_right_possible(array):
            self.to_right()
            self.state += 1
        elif self.state == 1 and self.to_up_possible(array):
            self.to_up()
            self.state += 1
        elif self.state == 2 and self.to_left_possible(array):
            self.to_left()
            self.state += 1
        elif self.state == 3 and self.to_down_possible(array):
            self.to_down()
            self.state += 1
        self.state %= 4

    def to_right_possible(self, array):
        # reference block is the one who remains in the same position every time
        x, y = self.pos[2]
        # block is upper the gameboard
        if y - 1 < 0:
            return True
        # block already taken
        elif array[x][y + 1] != -1:
            return False
        return True

    def to_right(self):
        x, y = self.pos[1]
        self.pos = [[x, y - 1], [x, y], [x, y + 1], [x + 1, y]]

    def to_up_possible(self, array):
        # reference block is the one who remains in the same position every time
        x, y = self.pos[1]
        # right wall
        if x - 1 < 0:
            return False
        # block taken
        elif array[x - 1][y] != -1:
            return False
        return True

    def to_up(self):
        x, y = self.pos[1]
        self.pos = [[x - 1, y], [x, y], [x + 1, y], [x, y - 1]]

    def to_left_possible(self, array):
        # reference block is the one who remains in the same position every time
        x, y = self.pos[1]
        # bottom reached
        if y + 1 >= 20:
            return False
        # block taken
        elif array[x][y + 1] != -1:
            return False
        return True
    
    def to_left(self):
        x, y = self.pos[1]
        self.pos = [[x - 1, y], [x, y], [x, y + 1], [x, y - 1]]

    def to_down_possible(self, array):
        # reference block is the one who remains in the same position every time
        x, y = self.pos[1]
        # right side reached
        if x + 1 >= 10:
            return False
        # block taken
        elif array[x + 1][y] != -1:
            return False
        return True

    def to_down(self):
        x, y = self.pos[1]
        self.pos = [[x - 1, y], [x, y], [x + 1, y], [x, y + 1]]