class Block:
    def __init__(self, typ):
        self.typ = typ
        self.fixed = False
        self.block = None
        if typ == 0:
            self.block = iBlock()
