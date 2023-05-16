# Console viewer for mergelife using micropython

import os
import mergelife
from vmatrix import vmatrix
import time
import sys

HEIGHT = 15
WIDTH = 20
dtime = .1
ctime = time.time()

try:
    rule = sys.argv[1]
    rule = rule.replace('-', '')
    rule = bytes.fromhex(rule)
except:
    rule = os.urandom(16)
ml_inst = mergelife.new_ml_instance(HEIGHT, WIDTH, rule)

nlines = 15
# scroll up to make room for output
print(f"\033[{nlines}S", end="")

# move cursor back up
print(f"\033[{nlines}A", end="")

# save current cursor position
print("\033[s", end="")

vmatrix.printmatrix(ml_inst['lattice'][0]['data'])
while True:
    if time.time() - ctime >= dtime:
        ctime = time.time()
        print("\033[u", end="")
        vmatrix.printmatrix(mergelife.update_step(ml_inst))