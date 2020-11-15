from .blocktypes.i_block import iBlock

class Block:
    def __init__(self, typ):
        self.typ = typ
        self.fixed = False
        self.block = None
        if typ == 0:
            self.block = iBlock()

    def move(self, array, x, y):
        if self.move_possible(array, x, y):
            self.block.pos = [[pos[0] + x, pos[1] + y] for pos in self.block.pos]
        elif x == 0 and y == 1:
            self.fixed = True

    def move_possible(self, array, x, y):
        for pos in self.block.pos:
            # x in bounds
            if pos[0] + x >= 10 or pos[0] + x < 0:
                return False
            # y in bounds
            elif pos[1] + y >= 20 or pos[1] + y < 0:
                return False
            # block in the way
            elif array[pos[0] + x][pos[1] + y] != -1:
                return False
        return True
