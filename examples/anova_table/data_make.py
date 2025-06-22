
from pathlib import Path
exercise_folder = Path(__file__).parent
print(exercise_folder)
import os
os.chdir(exercise_folder)

import pprint

from scipy.stats import f as f_dist
# https://chat.deepseek.com/a/chat/s/9014e41f-6f29-4028-9bde-ddc4c92fc8e9
from decimal import Decimal, ROUND_HALF_UP
def round_up_half(number, decimals=1):
    return float(Decimal(str(number)).quantize(Decimal(f'1e-{decimals}'), rounding=ROUND_HALF_UP))
#print(round_up_half(1.25))  # Output: 1.3
#print(round_up_half(1.35))  # Output: 1.4


def make(g, n, sqgrupos, sqerros):
    # Calculating Probability from the F-Distribution in Python
    # https://chat.deepseek.com/a/chat/s/f3e50569-f761-4df7-a3c7-b93fbda8cfc2
    dfgrupos = g-1
    dferros = g*n - g
    sqtotal = sqgrupos + sqerros 
    dftotal = dfgrupos + dferros
    msqgrupos = round_up_half(sqgrupos / dfgrupos, 3)
    msqerros = round_up_half(sqerros / dferros, 3)
    f = round_up_half(msqgrupos/msqerros, 3)
    sig = round_up_half(f_dist.sf(f, dfgrupos, dferros), 3)  # Survival function (1 - CDF)
    if sig < 0.05:
        rejeitarh0 = "existe pelo menos um valor esperado significativamente diferente"
    else:
        rejeitarh0 = "não existe diferença significativa entre os valores esperados"

    pprint.pprint(locals())
    return locals()

print(make(4, 6, 1000, 100))

# Adding a Row to a Pandas DataFrame from a Dictionary
# https://chat.deepseek.com/a/chat/s/b915bd68-18bc-4179-87c7-27059ae2c4a8


import pandas as pd
df = pd.DataFrame(make(4, 4,    4,  16), index=[0])
df.loc[len(df)] = make(4, 6, 1000, 100)
df.loc[len(df)] = make(4, 5,  500, 480)
df.loc[len(df)] = make(5, 5,  180, 170*5*5)
df.loc[len(df)] = make(4, 4,  200, 120)

#print(df)


df.to_excel("data.xlsx")


