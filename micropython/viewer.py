import os
import mergelife
from vmatrix import vmatrix

HEIGHT = 15
WIDTH = 20

rule = os.urandom(16)
ml_inst = mergelife.new_ml_instance(HEIGHT, WIDTH, rule)
while True:
    vmatrix.printmatrix(mergelife.update_step(ml_inst))