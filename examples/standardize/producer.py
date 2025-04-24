# --------------------------
# cloze_manyfiles_5_tabela
# --------------------------

from pathlib import Path
print(Path(__file__).parent)

#
# Equations or generic relations
#
scenario_relations = {
    "Eq(mean,  (x1+x2+x3)/3 )",
    "Eq(variance, ( (x1-mean)**2 + (x2-mean)**2 + (x3-mean)**2 )/3 )",
    "Eq(cv,   variance/mean)",
}

#
# 6 variables: description of each variable controls the way they appear
# 


variable_attributes = {
    "x1":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "x2":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "x3":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "mean": {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "variance": {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "cv":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
}

from numpy import sqrt
from scipy.stats import f as f_dist
# https://chat.deepseek.com/a/chat/s/9014e41f-6f29-4028-9bde-ddc4c92fc8e9
from decimal import Decimal, ROUND_HALF_UP
def round_up_half(number, decimals=1):
    return float(Decimal(str(number)).quantize(Decimal(f'1e-{decimals}'), rounding=ROUND_HALF_UP))
#print(round_up_half(1.25))  # Output: 1.3
#print(round_up_half(1.35))  # Output: 1.4

def make(x1,x2,x3):
    mean = 1/3*(x1+x2+x3)
    variance = (1/2)*( (x1-mean)**2 + (x2-mean)**2 + (x3-mean)**2 )
    cv = sqrt(variance)/mean
    return locals()
print(make(1.0, 2.0, 3.0))


# Adding a Row to a Pandas DataFrame from a Dictionary
# https://chat.deepseek.com/a/chat/s/b915bd68-18bc-4179-87c7-27059ae2c4a8


import pandas as pd
df = pd.DataFrame(make(1.0, 2.0, 3.0), index=[0])
df.loc[len(df)] = make(2.0, 2.0, 4.0)
df.loc[len(df)] = make(3.0, 2.0, 5.0)
df.loc[len(df)] = make(4.0, 2.0, 6.0)
df.loc[len(df)] = make(5.0, 2.0, 7.0)   


print(df)


df.to_excel(r"C:\Users\pedrocruz\Documents\GitHub\pyequa\examples\mean_variance\data.xlsx")

from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

pe.scenario.draw_wisdom_graph()


#import cProfile

# Profile the function
#profiler = cProfile.Profile()
#profiler.enable()



# Learning from the same exercises for everybody
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 1, 
#                           number_of_problems_per_givenvars = 1)



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


# Teacher can read and choose
pe.hard_first(max_number_of_problems=None, 
              max_combinations_givenvars_per_easynesslevel=2, 
              number_of_problems_per_givenvars=1)


#profiler.disable()
#profiler.print_stats(sort='time')  # Sort by time spent


"""
caso dificil

# Problem 001 (data row is 01) ((x3, variance, cv))

Consider the following sample,

* \(x_1\)={:NUMERICAL:%100%1:0.05}
* \(x_2\)={:NUMERICAL:%100%2:0.05}
* \(x_3\)=**3.0**
 
and based on this sample, the following statistics are calculated:

* \(\bar x\) = {:NUMERICAL:%100%2.0:0.05}
* \(\sigma^2\) = **0.6666666666666666**
* variation coefficient = **0.3333333333333333**
"""

