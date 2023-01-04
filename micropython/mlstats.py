from ulab import np as np

def avg(arr, height, width):
    avg_arr = np.zeros((height, width), dtype=np.uint8)
    for row in range(height):
        for col in range(width):
            avg_arr[row][col] = (arr[row][col][0] + arr[row][col][1] + arr[row][col][2]) / 3
    return avg_arr

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