# https://github.com/v923z/micropython-ulab
# Will support dot, copy, sum, convolve

# Simulator https://wokwi.com/projects/322595929479709267

from ulab import numpy as np
import ulab
from vmatrix import colors
import random

# from scipy.ndimage import convolve
# import scipy
# import scipy.stats
# import ctypes

# Return twos complement of val
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

# Convert signed byte to percent
def to_percent(val):
    if val > 0:
        return val / 127.0
    else:
        return val / 128.0

# Generate (rng, pct, i) tuples from rule
# Range is a byte converted to 0-2040, pct is signed byte converted to -1.0 to 1.0
# List is sorted by ascending range
def parse_rule(rule):
    print(rule.hex())
    switch = True
    code = []
    rng = None
    pct = None
    i = 0
    for b in rule:
        if switch:
            rng = b * 8
            if rng == 2040:
                rng = 2048
            switch = False
        else:
            pct = twos_comp(b, 8)
            pct = to_percent(pct)
            switch = True
            code.append((rng, pct, i))
            i += 1
    return sorted(code)

# Does some stats to calculate the next frame
def update_step(ml_instance):
    kernel = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    THIRD = 1.0 / 3.0

    # Get important values
    sorted_rule = ml_instance['sorted_rule']
    switch = ml_instance['switch']
    
    ml_instance['switch'] = not switch

    # Get current and previous lattice
    if switch:
        prev_data = ml_instance['lattice'][0]['data']
        current_data = ml_instance['lattice'][1]['data']
    else:
        prev_data = ml_instance['lattice'][1]['data']
        current_data = ml_instance['lattice'][0]['data']

    # Merge RGB
    data_avg = np.dot(prev_data, [THIRD, THIRD, THIRD]) # Average RGB of each pixel
    data_avg = data_avg.astype(int)
    pad_val = scipy.stats.mode(data_avg, axis=None)[0] # Mode of all averages
    pad_val = int(pad_val)
    data_cnt = convolve(data_avg, kernel, cval=pad_val, mode='constant') # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.convolve.html

    # Perform update
    previous_limit = 0
    for limit, pct, cidx in sorted_rule:
        mask = np.logical_and(data_cnt < limit, data_cnt >= previous_limit)
        previous_limit = limit

        if pct < 0:
            pct = abs(pct)
            cidx = (cidx + 1) % len(colors.COLOR_TABLE)

        # Moves the color towards the target color
        d = colors.COLOR_TABLE[cidx] - prev_data[mask]
        current_data[mask] = prev_data[mask] + np.floor(d * pct)

        # Save stats for calculating activity
        if switch:
            ml_instance['lattice'][0]['eval'] = {
                'mode': pad_val,
                'merge': data_avg,
            }
        else:
            ml_instance['lattice'][1]['eval'] = {
                'mode': pad_val,
                'merge': data_avg,
            }

    ml_instance['time_step'] += 1
    return current_data

def random_data(height, width):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for r in range(height):
        for c in range(width):
            data[r][c][0] = random.randint(0, 255)
            data[r][c][1] = random.randint(0, 255)
            data[r][c][2] = random.randint(0, 255)
    return data

def randomize_lattice(ml_instance):
    height = ml_instance['height']
    width = ml_instance['width']
    ml_instance['track'] = {}
    ml_instance['time_step'] = 0
    print(f"ulab version: {ulab.__version__}")
    ml_instance['lattice'][0]['data'] = random_data(height, width)
    ml_instance['lattice'][1]['data'] = ml_instance['lattice'][0]['data'].copy()

# Create a new instance of the merge life simulation
def new_ml_instance(height, width, rule):
    result = {
        'height': height,
        'width': width,
        'sorted_rule': parse_rule(rule),
        'time_step': 0,
        'switch' : False,
        'track': {},
        'lattice': [
            {'data': None, 'eval': None},
            {'data': None, 'eval': None}
        ]
    }

    randomize_lattice(result)
    return result

def calc_activity(ml_instance):
    height = ml_instance['height']
    width = ml_instance['width']
    time_step = ml_instance['time_step']

    d2_avg = ml_instance['lattice'][1]['eval']['merge']
    md2 = ml_instance['lattice'][1]['eval']['mode']

    mode_mask = (d2_avg == md2)

    # how long ago was a pixel the mode
    if 'eval-last-mode' in ml_instance['track']:
        last_mode = ml_instance['track']['eval-last-mode']
    else:
        last_mode = np.zeros((height, width), dtype=np.int)
        ml_instance['track']['eval-last-mode'] = last_mode

    last_mode[mode_mask] = time_step


    # Find the active cells
    # An active cell has not been a background cell for 5 steps, but was a background cell in the last 25 steps
    if time_step >= 25:
        t = (ml_instance['time_step'] - last_mode)
        t = np.logical_and(t > 5, t < 25)
        active_cnt = np.sum(t)
    else:
        active_cnt = 0

    size = height * width

    active_cnt /= size

    return active_cnt
