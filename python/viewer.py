import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import mergelife
from secrets import token_hex

STATIC_LIMIT = 25

class viewer:
    def __init__(self, rows, cols, interval=100):
        self.rows = rows
        self.cols = cols
        self.interval = interval
        self.fig = plt.figure()
        self.i = 0
        self.data = [None] * STATIC_LIMIT
        self.data[self.i] = np.random.randint(0,256, size=(self.rows, self.cols, 3), dtype=np.uint8)
        self.im = plt.imshow(self.data[self.i], animated=True)
        self.static_cnt = 0
        self.create_ml_inst(None)

    def create_ml_inst(self, event):
        rule = self.gen_rule()
        self.ml_inst = mergelife.new_ml_instance(self.rows, self.cols, rule)

    def updatefig(self, *args):
        self.update_i()
        self.data[self.i] = mergelife.update_step(self.ml_inst)
        if self.detect_static_rule():
            self.create_ml_inst(None)
        self.im.set_array(self.data[self.i])
        return self.im, # Theres a comma here for some reason

    def go_animate(self):
        pos = self.fig.add_axes([.8, 0.05, 0.1, 0.075])
        button = Button(pos, 'Next')
        button.on_clicked(self.create_ml_inst)
        ani = animation.FuncAnimation(self.fig, self.updatefig, interval=self.interval, blit=True)
        plt.show()
    
    def gen_rule(self):
        return token_hex(16)

    def update_i(self):
        self.i += 1
        self.i = self.i % STATIC_LIMIT
    
    def detect_static_rule(self):
        if mergelife.calc_activity(self.ml_inst) == 0:
            self.static_cnt += 1
            if self.static_cnt > STATIC_LIMIT:
                self.static_cnt = 0
                return True
        return False