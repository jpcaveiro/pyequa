
#
# Equations or generic relations
#
scenario_relations = {
    "Eq(Y_Distribution, nweekdays+probsucess)",                 
    "Eq(prob, nweekdays+probsucess+y_value)",     
}


#
# 6 variables: description of each variable controls the way they appear
# 
variable_attributes = {
    # Inteiros
    'nweekdays': {'type': 'numerical', 'tol': 0,    'givenvarlevel': 1},
    'y_value':      {'type': 'numerical', 'tol': 0,    'givenvarlevel': 1},
    # Reais
    'probsucess': {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 1},
    'prob':  {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 2},
    # Multichoice com distratores
    'Y_Distribution': {'type': 'multichoice', 'givenvarlevel': 2, 
                       'distractors': {'distractor_d1': '-33.333', 
                                       'distractor_d2': '-33.333', 
                                       'distractor_d3': '-33.333'}},
    # Distratora pura (não é variável de interesse ao problema)
    'n_packs': {'type': 'distractor'},
}


# MOODLE: Not all discounts
# https://docs.moodle.org/405/en/Import_questions
# minus or plus from
#    100, 90, 80, 75, 70, 66.666, 60, 50, 40, 33.333, 30, 25, 20, 16.666, 14.2857, 12.5, 11.111, 10, 5, 0


from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

# Learning from the same exercises for everybody
pe.exploratory()


# Teacher can read and choose
pe.hard_first(max_number_of_problems=4, max_combinations_givenvars_per_easynesslevel=None) # is the same as


