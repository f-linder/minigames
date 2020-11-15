class iBlock:
    def __init__(self):
        self.state = 0
        self.num_states = 2
        # state = 0 -> horizontal
        # state = 1 -> vertical
        self.pos = [[x, 0] for x in range(3, 7)]
    
    def change_state(self, array):
        if self.state == 0 and self.to_vertical_possible(array):
            self.to_vertical()
            self.state += 1
        elif self.state == 1 and self.to_horizontal_possible(array):
            self.to_horizontal()
            self.state += 1
        self.state %= 2

    def to_vertical(self):
        # reference block, 2nd to the left
        pos = self.pos[1]
        self.pos = [[pos[0], y] for y in range(pos[1] - 1, pos[1] + 3)]

    def to_vertical_possible(self, array):
        # reference block, 2nd to the left when horizontal
        pos = self.pos[1]

        # block below
        # bounds
        if pos[1] + 1 < 0:
            return False
        # free
        if array[pos[0]][pos[1] + 1] != -1:
            return False
        # two blocks above
        # free (bounds not needed)
        if array[pos[0]][pos[1] + 1] != -1 or array[pos[0]][pos[1] + 2] != -1:
            return False

        return True

    def to_horizontal(self):
        # reference block, 2nd from below when vertical
        pos = self.pos[1]
        self.pos = [[x, pos[y]] for x in range(pos[0] - 1, pos[1] + 2)]

    def to_horizontal_possible(self, array):
        # refrence block, 2nd from below when vertical
        pos = self.pos[1]

        # bounds to left and right
        if pos[0] - 1 < 0 or pos[0] + 1 >= 10 or pos[0] + 2 >= 10:
            return False
        # free to the left and right
        if array[pos[0] - 1][pos[1]] != -1 or array[pos[0] + 1][pos[1]] != -1 or array[pos[0] + 2][pos[1]] != -1:
            return False
        
        return True
    