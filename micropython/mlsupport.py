from ulab import numpy as np

# Returns array of intensities
def avg(arr, height, width):
    avg_arr = np.zeros((height, width), dtype=np.uint8)
    for row in range(height):
        for col in range(width):
            avg_arr[row][col] = (arr[row][col][0] + arr[row][col][1] + arr[row][col][2]) / 3
    return avg_arr

# Returns mode value in 2d array
def mode(arr):
    freq = {}
    for row in arr:
        for avg in row:
            freq.setdefault(avg, 0)
            freq[avg] += 1
         
    hf = max(freq.values())

    for i, j in freq.items():
        if j == hf:
            return i

# Returns array where each element is the sum of its neighbors (padded with pad_val)
def count_neighbors(arr,  pad_val, height, width):
    new_arr = np.zeros((height, width), dtype=np.uint16)
    for row in range(height):
        for col in range(width):
            sum = 0
            sum += get_neighbor(arr, row - 1, col - 1, pad_val)
            sum += get_neighbor(arr, row - 1, col, pad_val)
            sum += get_neighbor(arr, row - 1, col + 1, pad_val)
            sum += get_neighbor(arr, row, col - 1, pad_val)
            sum += get_neighbor(arr, row, col + 1, pad_val)
            sum += get_neighbor(arr, row + 1, col - 1, pad_val)
            sum += get_neighbor(arr, row + 1, col, pad_val)
            sum += get_neighbor(arr, row + 1, col + 1, pad_val)
            new_arr[row][col] = sum
    return new_arr

# Returns neighbor value or pad_val if out of bounds
def get_neighbor(arr, row, col, pad_val):
    try:
        return arr[row][col]
    except IndexError:
        return pad_val

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