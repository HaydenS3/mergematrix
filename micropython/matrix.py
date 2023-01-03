# Colors to be used for printing the matrix
class colors:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    yellow = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    white = '\033[47m'

class matrix:
    # Prints a color to the terminal
    def printcolor(color):
        print(color, end=' ')
    # Prints a matrix to the terminal
    def printmatrix(matrix):
        print("do something")