
#
# Equations or generic relations
#
scenario_relations = {
    "Eq(numb1+b1, numb2+b2)",                 
}


#
# 6 variables: description of each variable controls the way they appear
# 

# converters
from numpy import int64
from numpy import float64

variable_attributes = {
    # Inteiros
    'numb1': {'type': 'multichoice',   'givenvarlevel': 1},
    'b1':    {'type': 'multichoice',   'givenvarlevel': 1},
    'numb2': {'type': 'multichoice',   'givenvarlevel': 2},
    'b2':    {'type': 'multichoice',   'givenvarlevel': 1},
}

# IDEIA: obter atributos de "variable_attributes" lendo o conteúdo de um pandas:

"""TODO: gerar aqui no Python
import pandas as pd
import numpy as np

# Create sample data (lists of strings)
data = {
    'numb1': [],
    'Column2': ['red', 'yellow', 'red', 'brown', 'purple'],
    'Column3': ['round', 'long', 'small', 'oval', 'small'],
    'Column4': ['sweet', 'tart', 'sweet', 'sweet', 'tart']
}

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
print(df)
"""


# MOODLE: Not all discounts
# https://docs.moodle.org/405/en/Import_questions
# minus or plus from
#    100, 90, 80, 75, 70, 66.666, 60, 50, 40, 33.333, 30, 25, 20, 16.666, 14.2857, 12.5, 11.111, 10, 5, 0


from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

# Learning from the same exercises for everybody
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 2, 
#                           number_of_problems_per_givenvars = 2,
#)


# Learning using "moodle random questions" based in a similar level
#pe.challenge_with_randomquestions(max_combinations_givenvars_per_easynesslevel = 2)



# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
#pe.exam_with_randomquestions(fill_in_blanks_vars = {'probvalory', 'probsemanas'}, 
#                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
pe.exploratory() # is the same as
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)


