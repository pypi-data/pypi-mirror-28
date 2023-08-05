from modelx import *

# model, space = new_model(), new_space()
#
# @defcells
# def testfunc(x, y):
#     if x == 0:
#         return y
#     if y == 0:
#         return x
#     else:
#         return (testfunc(x - 1, y) ** 2 + testfunc(x , y - 1) ** 2) ** 0.5
#
#
# testfunc[1, 1]
# # testfunc[None, 1] = 3
# testfunc.series
#
# @defcells
# def testfunc2(t):
#     return testfunc(t, t)
#
# testfunc2(1)

import pandas as pd
import numpy as np


df = pd.DataFrame({'AAA': [4,5,6,7],
                   'NNN': [np.nan]*4,
                   'MMM': [np.nan]*4,
                   'BBB': [10,20,30,40],
                   'CCC': [100,50,-30,-50]})

df.set_index(['BBB', 'NNN', 'MMM'], inplace=True)

# for i, idx in enumerate(df.index.levels):
#     if idx.size == 0:
#         df.drop()

# nan_idx = []
# for idx in df.index.levels:
#     if idx.size == 0:
#         nan_idx.append(idx.name)
#
# df.index.drop()

def reset_naindex(df):

    nan_levels = [lv for lv, idx in enumerate(df.index.levels)
                  if idx.size == 0]

    for i, lv in enumerate(nan_levels):
        name = df.index.levels[lv - i].name
        df.index = df.index.droplevel(lv - i)
        df.insert(0, name, np.nan)

    return df

