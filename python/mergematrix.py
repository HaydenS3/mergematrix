from secrets import token_hex
from viewer import viewer

HEIGHT = 15
WIDTH = 20
INTERVAL = 100

def gen_rule():
    return token_hex(16)

myviewer = viewer(HEIGHT, WIDTH, gen_rule(), INTERVAL)
myviewer.go_animate()