### Install

- For ulab: `./build.sh 3`. Builds ulab for 3 dimensioned arrays.
- Had to replace all `STATIC` with `static` to compile. See [this](https://github.com/micropython/micropython/wiki/Build-Troubleshooting)

### Stats

Working on a function to detect non-interesting displays and automatically generate a new one. Analyzing Heaton's stats to see which stats can be used.

- mage: How long has the mode been its value
- mode: Most common pixel color
- mc: Count of pixels that have been mode for > 5 iterations
- bg: mc / # of pixels
- cnt_fg: Count of pixels that have been same for > 5 iterations
- fg: cnt_fg / # of pixels
- cnt_act: Count of active cells. An active cell has not been a background cell for 5 steps, but was a background cell in the last 25 steps
- act: cnt_act / # of pixels (**This is the stat we want**)
- chaos: ((height \* width) - (cnt_bg + cnt_fg + cnt_act)) / # of pixels

### Memory Usage

- lattice.1.data: 900 bytes
- lattice.0.data: 900 bytes
- color table: 24 bits (3 bytes)
- code: 16 bytes
- sorted code: 56 bytes
- kernel: 9 bits (2 bytes)
- height: 1 byte
- width: 1 byte
- data_avg: 300 bytes
- pad_val: 1 byte
- data_cnt: 300 bytes
- mask: 300 bits (38 bytes)
- d: 900 bytes
- mode_mask: 300 bits (38 bytes)
- last_mode: 300 bytes

### Importing ndimage into ulab's scipy

- `__init__.py` **(Needs to be edited to reflect below)**
- `_filters.convolve`
- `_filters._correlate_or_convolve`
- `_ni_support._get_output`
- `_filters._complex_via_real_components`
- `_ni_support._normalize_sequence`
- `_filters._invalid_origin`
- `_ni_support._extend_mode_to_code`
- `_filters.correlate`

### Running

```
cd micropython
./micropython viewer.py
```
