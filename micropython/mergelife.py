# https://github.com/v923z/micropython-ulab
# Will support dot, copy, sum, convolve

# Simulator https://wokwi.com/projects/322595929479709267

from ulab import numpy as np
from vmatrix import colors
import random
import mlsupport
from ulab import scipy

# from scipy.ndimage import convolve
# import scipy.stats
# import ctypes

# Generate (rng, pct, i) tuples from rule
# Range is a byte converted to 0-2040, pct is signed byte converted to -1.0 to 1.0
# List is sorted by ascending range
def parse_rule(rule):
    print(rule.hex())
    current = True
    code = []
    rng = None
    pct = None
    i = 0
    for b in rule:
        if current:
            rng = b * 8
            if rng == 2040:
                rng = 2048
            current = False
        else:
            pct = mlsupport.twos_comp(b, 8)
            pct = mlsupport.to_percent(pct)
            current = True
            code.append((rng, pct, i))
            i += 1
    return sorted(code)

# Does some stats to calculate the next frame
def update_step(ml_instance):
    # Get important values
    height = ml_instance['height']
    width = ml_instance['width']
    sorted_rule = ml_instance['sorted_rule']
    current = ml_instance['current']
    
    ml_instance['current'] = not current

    prev_data = ml_instance['lattice'][not current]['data']
    current_data = ml_instance['lattice'][current]['data']

    # Merge RGB
    data_avg = mlsupport.avg(prev_data, height, width)
    pad_val = mlsupport.mode(data_avg)
    data_cnt = mlsupport.count_neighbors(data_avg, pad_val, height, width)

    # Perform update
    previous_limit = 0
    for limit, pct, cidx in sorted_rule:
        current_data = update_data(current_data, prev_data, data_cnt, limit, previous_limit, pct, cidx, height, width)
        previous_limit = limit

        # TODO: This may need to change to `current`
        ml_instance['lattice'][not current]['eval'] = {
            'mode': pad_val,
            'merge': data_avg,
        }
    ml_instance['time_step'] += 1
    ml_instance['lattice'][not current]['data'] = current_data
    return current_data

# Generate random data
def random_data(height, width):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for r in range(height):
        for c in range(width):
            data[r][c][0] = random.randint(0, 255)
            data[r][c][1] = random.randint(0, 255)
            data[r][c][2] = random.randint(0, 255)
    return data

# Randomize the lattices
def randomize_lattice(ml_instance):
    height = ml_instance['height']
    width = ml_instance['width']
    ml_instance['lattice'][0]['data'] = random_data(height, width)
    ml_instance['lattice'][1]['data'] = ml_instance['lattice'][0]['data'].copy()

# Create a new instance of the merge life simulation
def new_ml_instance(height, width, rule):
    result = {
        'height': height,
        'width': width,
        'sorted_rule': parse_rule(rule),
        'time_step': 0,
        'current' : False,
        'track': {},
        'lattice': [
            {'data': None, 'eval': None},
            {'data': None, 'eval': None}
        ]
    }

    randomize_lattice(result)
    return result

def update_data(current_data, prev_data, data_cnt, limit, previous_limit, pct, cidx, height, width):    
    if pct < 0:
            pct = abs(pct)
            cidx = (cidx + 1) % len(colors.COLOR_TABLE)

    new_data = current_data.copy()
    for r in range(height):
        for c in range(width):
            if data_cnt[r][c] >= previous_limit and data_cnt[r][c] < limit:
                d = colors.COLOR_TABLE[cidx] - prev_data[r][c]
                new_data[r][c] = prev_data[r][c] + np.floor(d * pct)
    return new_data

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
