# --------------------------
# cloze_manyfiles_5_tabela
# --------------------------

from pathlib import Path
print(Path(__file__).parent)

#
# Equations or generic relations
#
scenario_relations = {
    "Eq(dfgrupos,g-1)",
    "Eq(dferros,g*n-g)",
    "Eq(sqtotal,   sqgrupos+sqerros)",
    "Eq(dftotal,   dfgrupos+dferros)",
    "Eq(msqgrupos, sqgrupos/dfgrupos)",
    "Eq(msqerros,  sqerros/dferros)",
    "Eq(f,         msqgrupos/msqerros)",
    "Eq(sig,       f)",
}


#
# 6 variables: description of each variable controls the way they appear
# 


variable_attributes = {
    'g': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'n': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'sqgrupos': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'sqerros': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'sqtotal': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'dfgrupos': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'dferros': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'dftotal': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 2},
    'msqgrupos': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'msqerros': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'f': {'type': 'numerical', 'tol': 0.005,  'givenvarlevel': 2},
    'sig': {'type': 'numerical', 'tol': 0.005,  'givenvarlevel': 2},
}

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
    return locals()
print(make(4, 6, 1000, 100))

# Adding a Row to a Pandas DataFrame from a Dictionary
# https://chat.deepseek.com/a/chat/s/b915bd68-18bc-4179-87c7-27059ae2c4a8


import pandas as pd
df = pd.DataFrame(make(4,4,4,4), index=[0])
df.loc[len(df)] = make(4, 6, 1000, 100)
df.loc[len(df)] = make(4, 5,  500, 480)
df.loc[len(df)] = make(5, 5,  180, 170)
df.loc[len(df)] = make(4, 4,  200, 120)

print(df)


df.to_excel("data.xlsx")



from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

# Learning from the same exercises for everybody
pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 1, 
                           number_of_problems_per_givenvars = 1)


# Learning using "moodle random questions" based in a similar level
#pe.challenge_with_randomquestions(max_combinations_givenvars_per_easynesslevel = 2)



# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
#pe.exam_with_randomquestions(fill_in_blanks_vars = {'probvalory', 'probsemanas'}, 
#                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
#pe.exploratory() # is the same as
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)
