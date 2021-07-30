from gameboard import *


class MyPlayer:

    #CREATOR

    def __init__(self, width, height):
        self._b = GameBoard(Shape(width, height))



    #METHODS FOR PRINTING THE BOARD PROPERLY


    def __str__(self):
        """Converts the boolean matrix into a string, a false square it's a black square and
        a true square it's a white square"""
        return self._b.__str__()

        #O(__str__ function)



    def __repr__(self):
        """Reports: size of the board and the squares with tokens"""
        return self._b.__repr__()

        #O(__repr__ function)




    #MODIFIERS



    def place_block (self, location, subshape = Shape(1,1)):
        """Returns the board with the block given placed in it or the board without beeing modified if the block
        can't be placed"""

        assert self._b.is_empty(location, subshape), "The block could not be placed. The board has not been modified."

        #The block can be placed
        self._b.put(location, subshape)

        fullcols = self._b.full_columns()
        fullrows = self._b.full_rows()

        #delete the full columns and the full rows, we previously copy the value
        #because when we delete the full columns then it can miss a token from a full row
        self._b.clear_columns(fullcols)
        self._b.clear_rows(fullrows)

        return self

        #O(max{board's height, board's width})



    def play(self, bl):
        """From all the possible locations for a block, returns the one with the lowest row.
        In case several locations are possible in the same row, returns the one with the lowest column.
        If there's no possible location, it returns None"""

        return self._simple(bl)

        #O(board's height * board's width)



    #CHECKER



    def is_legal(self,bl):
        """Returns true if the blocks are legal"""
        #check each concept: the block must be a Shape, the shapes must be positive integers
        return isinstance(bl, Shape) and \
            isinstance(bl.width, int) and \
            isinstance(bl.height, int) and \
            bl.width > 0 and \
            bl.height > 0




    #PRIVATE


    def _simple(self, bl):
        """Game's algorithm"""

        assert self.is_legal(bl), "The block is not legal"

        num_rows = self._b._shape.height
        num_cols = self._b._shape.width

        for r in range(num_rows - bl.height+1) :
            #do not check a row nor a columns in which doesn't fit the block, optimization
            for c in range(num_cols - bl.width+1) :
                if self._b.is_empty(Location(r,c), bl) :
                    return Location(r,c)

        return None

        #O(board's height * board's width)
