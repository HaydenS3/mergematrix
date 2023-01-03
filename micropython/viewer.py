import os
import mergelife

HEIGHT = 15
WIDTH = 20

rule = os.urandom(16)
ml_inst = mergelife.new_ml_instance(HEIGHT, WIDTH, rule)

