from .blocktypes.i_block import iBlock
from .blocktypes.o_block import oBlock
from .blocktypes.t_block import tBlock
from .blocktypes.l_block import lBlock
from .blocktypes.j_block import jBlock

class Block:
    def __init__(self, typ):
        self.typ = typ
        self.fixed = False
        self.block = None
        if typ == 0:
            self.block = iBlock()
        elif typ == 1:
            self.block = oBlock()
        elif typ == 2:
            self.block = tBlock()
        # normally 5
        elif typ == 3:
            self.block = lBlock()
        # normally 6
        elif typ == 4:
            self.block = jBlock()

    def move(self, array, x, y):
        if self.move_possible(array, x, y):
            self.block.pos = [[pos[0] + x, pos[1] + y] for pos in self.block.pos]
        elif x == 0 and y == 1:
            for pos in self.block.pos:
                # floor reached or first line
                if pos[1] + y >= 20 or pos[1] + y < 0:
                    self.fixed = True
                    break
                elif array[pos[0]][pos[1] + y] != -1:
                    self.fixed = True
                    break

    def move_possible(self, array, x, y):
        for pos in self.block.pos:
            # x in bounds
            if pos[0] + x >= 10 or pos[0] + x < 0:
                return False
            # y in bounds
            elif pos[1] + y >= 20:
                return False
            elif pos[1] + y < 0:
                continue
            # block in the way
            elif array[pos[0] + x][pos[1] + y] != -1:
                return False
        return True

    def change_state(self, array):
        self.block.change_state(array)
