Working on a function to detect non-interesting displays and automatically generate a new one. Analyzing Heaton's stats to see which stats can be used.

Stats

- mage: How long has the mode been its value
- mode: Most common pixel color
- mc: Count of pixels that have been mode for > 5 iterations
- bg: mc / # of pixels
- cnt_fg: Count of pixels that have been same for > 5 iterations
- fg: cnt_fg / # of pixels
- cnt_act: Count of active cells. An active cell has not been a background cell for 5 steps, but was a background cell in the last 25 steps
- act: cnt_act / # of pixels (**This is the stat we want**)
- chaos: ((height \* width) - (cnt_bg + cnt_fg + cnt_act)) / # of pixels
