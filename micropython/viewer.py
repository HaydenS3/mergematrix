import os
import mergelife
from vmatrix import vmatrix

HEIGHT = 15
WIDTH = 20

rule = os.urandom(16)
ml_inst = mergelife.new_ml_instance(HEIGHT, WIDTH, rule)
data = ml_inst['lattice'][0]['data']
vmatrix.printmatrix(data)