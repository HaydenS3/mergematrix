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

    list = [black, red, green, yellow, blue, purple, cyan, white]

    def calc_color(rgb):
        rgb = rgb >> 7;
        

class vmatrix:
    # Prints a color to the terminal
    def printcolor(color):
        print(color, end=' ')
    # Prints a matrix to the terminal
    def printmatrix(matrix):
        for row in matrix:
            for column in row:
                printcolor(column)
            print()
    

class matrix:
    print("This will be used to control the physical matrix")