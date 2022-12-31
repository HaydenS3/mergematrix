import numpy as np
from scipy.ndimage import convolve
import scipy
import scipy.stats
import ctypes
from PIL import Image
import dp

# The color table.
COLOR_TABLE = [
    [0, 0, 0],  # Black 0
    [255, 0, 0],  # Red 1
    [0, 255, 0],  # Green 2
    [255, 255, 0],  # Yellow 3
    [0, 0, 255],  # Blue 4
    [255, 0, 255],  # Purple 5
    [0, 255, 255],  # Cyan 6
    [255, 255, 255]  # White 7
]


def parse_update_rule(code):
    code = fromHex(code)

    sorted_code = []
    for i, x in enumerate(code):
        rng = int(x[0] * 8)
        if x[1] > 0:
            pct = x[1] / 127.0
        else:
            pct = x[1] / 128.0
        sorted_code.append((2048 if rng == 2040 else rng, pct, i))

    sorted_code = sorted(sorted_code)
    return sorted_code


def update_step(ml_instance):
    kernel = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    THIRD = 1.0 / 3.0

    # Get important values
    sorted_rule = ml_instance['sorted_rule']
    height = ml_instance['height']
    width = ml_instance['width']
    changed = np.zeros((height, width), dtype=np.bool)

    # Swap lattice
    t = ml_instance['lattice'][1]
    ml_instance['lattice'][1] = ml_instance['lattice'][0]
    ml_instance['lattice'][0] = t

    # Get current and previous lattice
    prev_data = ml_instance['lattice'][1]['data']
    current_data = ml_instance['lattice'][0]['data']

    # Merge RGB
    data_avg = np.dot(prev_data, [THIRD, THIRD, THIRD])
    data_avg = data_avg.astype(int)
    pad_val = scipy.stats.mode(data_avg, axis=None)[0]
    pad_val = int(pad_val)
    data_cnt = convolve(data_avg, kernel, cval=pad_val, mode='constant')

    # Perform update
    for limit, pct, cidx in sorted_rule:
        mask = data_cnt < limit
        mask = np.logical_and(mask, np.logical_not(changed))
        changed = np.logical_or(changed, mask)

        if pct < 0:
            pct = abs(pct)
            cidx = cidx + 1
            if cidx >= len(COLOR_TABLE):
                cidx = 0

        d = COLOR_TABLE[cidx] - prev_data[mask]
        current_data[mask] = prev_data[mask] + np.floor(d * pct)
        ml_instance['lattice'][0]['eval'] = {
            'mode': pad_val,
            'merge': data_avg,
            'neighbor': data_cnt
        }

    ml_instance['time_step'] += 1
    return current_data

def fromHex(str):
    result = []
    str = str.replace('-', '')
    for i in range(len(COLOR_TABLE)):
        idx = i * 4
        rng = str[idx:idx + 2]
        pct = str[idx + 2:idx + 4]
        rng = int(rng, 16)
        pct = int(pct, 16)

        pct = ctypes.c_byte(pct).value  # Twos complement
        result.append((rng, pct))

    return result

def randomize_lattice(ml_instance):
    height = ml_instance['height']
    width = ml_instance['width']
    ml_instance['track'] = {}
    ml_instance['time_step'] = 0
    ml_instance['lattice'][0]['data'] = np.random.randint(0, 256, size=(height, width, 3), dtype=np.uint8)
    ml_instance['lattice'][1]['data'] = np.copy(ml_instance['lattice'][0]['data'])

def new_ml_instance(height, width, rule_str):
    result = {
        'height': height,
        'width': width,
        'rule_str': rule_str,
        'sorted_rule': parse_update_rule(rule_str),
        'time_step': 0,
        'track': {},
        'lattice': [
            {'data': None, 'eval': None},
            {'data': None, 'eval': None}
        ]
    }

    randomize_lattice(result)
    result['lattice'][1]['data'] = np.copy(result['lattice'][0]['data'])
    return result

def calc_activity(ml_instance):
    height = ml_instance['height']
    width = ml_instance['width']
    time_step = ml_instance['time_step']

    e1 = ml_instance['lattice'][0]['eval']
    e2 = ml_instance['lattice'][1]['eval']

    if e1 is None or e2 is None:
        return  0

    d2_avg = e2['merge']

    # What percent of the grid is the mode, what percent is the background
    md2 = e2['mode']

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
        t1 = t > 5
        t2 = t < 25
        t = np.logical_and(t1, t2)
        sp = np.sum(t)
    else:
        sp = 0

    size = height * width
    cnt_act = sp

    cnt_act /= size

    return cnt_act
