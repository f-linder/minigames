class zBlock():
    def __init__(self):
        self.state = 0
        self.num_states = 2
        # state 0 -> horizontal
        # state 1 -> vertival
        self.pos = [[4, 0], [5, 0], [4, -1], [3, -1]]

    def change_state(self, array):
        if self.state == 0 and self.to_vertical_possible(array):
            self.to_vertical()
            self.state += 1
        elif self.state == 1 and self.to_horizontal_possible(array):
            self.to_horizontal()
            self.state += 1
        self.state %= self.num_states

    def to_vertical_possible(self, array):
        x, y = self.pos[2]
        if y < 0:
            return True
        elif array[x + 1][y] != -1:
            return False
        elif y - 1 < 0:
            return True
        elif array[x + 1][y - 1] != -1:
            return False
        return True
    
    def to_vertical(self):
        x, y = self.pos[2]
        self.pos = [[x + 1, y - 1], [x + 1, y], [x, y], [x, y + 1]]

    def to_horizontal_possible(self, array):
        x, y = self.pos[2]
        if x - 1 < 0:
            return False
        elif array[x + 1][y + 1] != -1:
            return False
        elif y - 1 < 0:
            return True
        elif array[x - 1][y] != -1:
            return False
        return True

    def to_horizontal(self):
        x, y = self.pos[2]
        self.pos = [[x, y + 1], [x + 1, y + 1], [x, y], [x - 1, y]]