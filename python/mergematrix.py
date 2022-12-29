from viewer import viewer

ROWS = 15
COLS = 20
INTERVAL = 100

myviewer = viewer(ROWS, COLS, viewer.gen_rule(None), INTERVAL)
myviewer.go_animate()