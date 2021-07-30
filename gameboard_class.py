#27-03-21
from collections import namedtuple
Location = namedtuple('Location', 'row column')
Shape = namedtuple('Shape', 'width height')

class GameBoard:

    #CREATOR

    #c it's columns/width
    #r it's rows/height

    def __init__(self, shape):
        #check whether shape is a Shape data type
        assert isinstance(shape, Shape), "GameBoard needs a parameter of type Shape"

        #shape of the board
        self._shape = shape

        #the board is represented by a boolean matrix, each square is initialize
        #in False, which means there's no token init
        self._board = [[False for c in range (self._shape.width)] for r in range (self._shape.height)]

        #two arrays which contain the number of tokens per row and column
        self._columnes = [0 for c in range (self._shape.width)]
        self._files = [0 for r in range (self._shape.height)]
        #the goal of this two arrays is to increase the program's eficiency




    #METHODS FOR PRINTING THE BOARD PROPERLY



    def __str__(self):
        """Prints the board"""
        #Converts the boolean matrix into a string

        matrix_str = ""

        for r in range (self._shape.height - 1, -1, -1):
            #(0,0) it's the lower left square, so start printing from the last row to the first row
            #upside down
            for c in range (self._shape.width):
                if self._board[r][c]:
                    #true square means that there's a token --> black square
                    matrix_str += '\u2b1b'

                else:
                    #false square means that there isn't a token --> white square
                    matrix_str += '\u2b1c'

            matrix_str += '\n'
            #enter

        return matrix_str

        #O(board's height * board's width)



    def __repr__(self):
        """Reports the size of the board and the squares with tokens"""
        string = (str(self._shape.width) +  'x' + str(self._shape.height) + " board: {")

        first_item = True

        for r in range (self._shape.height):
            for c in range (self._shape.width):
                if self._board[r][c]:
                    #if there's a true square, there's a token, we print the position of the token
                    if first_item:
                        #presentation style
                        first_item = False

                    else:
                        string += ', '

                    string += ('(' + str(r) + ', ' + str(c) + ')')

        string += ('}')
        return string

        #O(board's height * board's width)




    #GETTER



    def get_shape(self):
        """Returns the dimensions of the board"""
        return self._shape
        ### O(1)




    #CONSULTOR METHODS

    #i: iterator for rows, heigth
    #j: iterator for columns, width

    def is_full (self, location, subshape=Shape(1,1)):
        """Checks whether a square is full or not"""
        #if we just recive a location, we assign a subshape of Shape(1,1), which means: just a single token
        #otherwise, the subshape takes the given value
        c = location.column
        r = location.row

        assert self._square_inside_board(r, c, subshape), "Location is out of the board"

        #The squares we have to check are inside the board
        for j in range(c, c + subshape.width):
            for i in range(r, r + subshape.height):
                if not self._board[i][j] :
                    #there isn't a token in the square checked --> it's empty
                    return False

        return True

        #O(subshape's width * subshape's height)



    def is_empty (self, location, subshape=Shape(1,1)):
        """Checks whether a square is empty or not"""
        #if we just recive a location, we assigne a subshape of Shape(1,1), which means: just a single token
        #otherwise, the subshape takes the values given
        c = location.column
        r = location.row

        assert self._square_inside_board(r, c, subshape), "Location is out of the board"

        #The squares we have to check are inside the board
        for j in range(c, c + subshape.width):
            for i in range(r, r + subshape.height):
                if self._board[i][j] :
                    #there's a token --> the square is full
                    return False

        return True

        #O(subshape's width * subshape's height)



    def full_rows(self) :
        """Returns a list of rows which are full"""
        list = []
        #empty list: we haven't found any full row

        for i in range(self._shape.height) :
            if self._files[i] == self._shape.width :
                #the number of tokens per row it's equal to the number of columns --> full row
                list.append(i)

        return list

        #O(board's height)



    def full_columns(self) :
        """Returns a list of columns which are full"""
        list = []
        #empty list: we haven't found any full column
        for j in range(self._shape.width) :
            #the number of tokens per column it's equal to the number of rows -->  full column
            if self._columnes[j] == self._shape.height:
                list.append(j)
        return list

        #O(board's width)



    def column_counters(self) :
        """Returns a list of the number of tokens in each column"""
        return self._columnes

        #O(1)



    def row_counters(self) :
        """Returns a list of the number of tokens in each row"""
        return self._files

        #O(1)




    #MODIFICATORS



    def put(self, location, subshape=Shape(1,1)) :
        """Returns the board with the tokens in the squares we have asked for or the board withou beeing modified
        if it's not possible to place it"""
        c = location.column #number of columns from left to right
        r = location.row #number of row from bottom to top

        assert self._square_inside_board(r, c, subshape), "The square is out of bounds"
        assert self.is_empty(location, subshape), "The square is already occupied."


        #we can put the tokens in the board
        for i in range(c, c + subshape.width):#column
            for j in range(r, r + subshape.height):#row
                self._board[j][i] = True
                self._files[j]+=1
                #we have added a token in the "j" row
                self._columnes[i]+=1
                #we have added a token in the "i" column

        return self

        #O(block's width * block's height)



    def remove(self, location, subshape=Shape(1,1)):
        """Removes a token from a square"""
        c = location.column
        r = location.row

        assert self._square_inside_board(r, c, subshape), "Location is out of the board"
        assert self.is_full(location, subshape), "There are empty squares"

        #the squares we want to remove have tokens, remove them
        for j in range(c, c + subshape.width):
            for i in range(r, r + subshape.height):
                self._board[i][j] = False
                self._files[i]-=1
                #we have removed a token from the "i" row
                self._columnes[j]-=1
                #we have removed a token from the "j" column

        return self

        #O(block's width * block's height)



    def clear_rows(self, list_rows):
        """Removes all tokens present in the rows given, regardless they are full or not"""
        for i in list_rows:
            for j in range(self._shape.width):
                if self._board[i][j] :
                    self._board[i][j] = False
                    self._columnes[j] -= 1
                    #if the square it's full (true), remove the token --> remove one from the "j" column
            self._files[i] = 0

        return self

        #O(given rows * board's width)



    def clear_columns(self, list_cols):
        """Removes all tokens present in the columns given, regardless they are full or not"""
        for j in list_cols:
            for i in range(self._shape.height):
                if self._board[i][j] :
                    self._board[i][j] = False
                    self._files[i] -= 1
            self._columnes[j] = 0
            #update the two arrays, columns and rows

        return self

        #O(given columns * board's height)



    #PRIVATE

    def _square_inside_board(self, r, c, subshape):
        """Checks whether the location and shape of the block are in the board or not"""
        return c >= 0 and \
            c + subshape.width  <= self._shape.width  and \
            r >= 0 and \
            r + subshape.height <= self._shape.height
