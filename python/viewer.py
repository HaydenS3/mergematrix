import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import mergelife
from secrets import token_hex
import time
import os, psutil

STATIC_LIMIT = 25
TIME_LIMIT = 60

class viewer:
    def __init__(self, rows, cols, interval=100):
        self.rows = rows
        self.cols = cols
        self.interval = interval
        self.fig = plt.figure()
        data = np.random.randint(0,256, size=(self.rows, self.cols, 3), dtype=np.uint8)
        self.im = plt.imshow(data, animated=True)
        self.create_ml_inst(None)
        self.time = time.perf_counter()

    def create_ml_inst(self, event):
        self.static_cnt = 0
        self.time = time.perf_counter()
        self.ml_inst = mergelife.new_ml_instance(self.rows, self.cols, self.gen_rule())

    def updatefig(self, *args):
        process = psutil.Process(os.getpid())
        print(process.memory_info().rss)

        data2 = mergelife.update_step(self.ml_inst)
        if self.detect_static_rule():
            self.create_ml_inst(None)
        if time.perf_counter() - self.time > TIME_LIMIT:
            self.create_ml_inst(None)
        self.im.set_array(data2)
        return self.im, # Theres a comma here for some reason

    def go_animate(self):
        pos = self.fig.add_axes([.8, 0.05, 0.1, 0.075])
        button = Button(pos, 'Next')
        button.on_clicked(self.create_ml_inst)
        ani = animation.FuncAnimation(self.fig, self.updatefig, interval=self.interval, blit=True)
        plt.show()
    
    def gen_rule(self):
        return token_hex(16)
    
    def detect_static_rule(self):
        if mergelife.calc_activity(self.ml_inst) == 0:
            self.static_cnt += 1
            if self.static_cnt > STATIC_LIMIT:
                return True
        return False