# Colors class to be used for printing the matrix
class colors:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    yellow = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    white = '\033[47m'
    
    reset = '\033[0m'

    list = [black, red, green, yellow, blue, purple, cyan, white]

    # The color table.
    COLOR_TABLE = [
        [0, 0, 0],      # Black 0
        [255, 0, 0],    # Red 1
        [0, 255, 0],    # Green 2
        [255, 255, 0],  # Yellow 3
        [0, 0, 255],    # Blue 4
        [255, 0, 255],  # Purple 5
        [0, 255, 255],  # Cyan 6
        [255, 255, 255] # White 7
    ]

    def calc_color(rgb):
        for i, intensity in enumerate(rgb):
            if intensity >= 128:
                rgb[i] = 255
            else:
                rgb[i] = 0
        index = colors.COLOR_TABLE.index(list(rgb))
        return colors.list[index]   

class vmatrix:
    # Prints a color to the terminal
    def printcolor(color):
        print(color, end=' ')
    # Print newline for matrix
    def print_new():
        print(colors.reset)
    # Prints a matrix to the terminal
    def printmatrix(matrix):
        for row in matrix:
            for color in row:
                vmatrix.printcolor(colors.calc_color(color))
            vmatrix.print_new()

# color_matrix = [
#                 [[121,55,39],[213,51,108],[46,150,20],[165,143,65]],
#                 [[44,114,220],[144,26,166],[112,155,184],[246,211,134]]
#                 ]

# vmatrix.printmatrix(color_matrix)