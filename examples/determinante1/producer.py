# --------------------------
# determinante1
# --------------------------

from pathlib import Path
print(Path(__file__).parent)

#
# Equations or generic relations
#
scenario_relations = {
    "Eq(d, a11*a22 - a12*a21)",
    "Eq(solucaounica, d)",
}    
    #"Eq(d, round_up_half(d, 3))", #TODO: alertar contra equação "auto regressiva": d=d!

#
# 6 variables: description of each variable controls the way they appear
# 


variable_attributes = {
    'a11': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'a12': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'a21': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'a22': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'd':   {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'solucaounica': {'type': 'multichoice', 'givenvarlevel': 2},
}


from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

#pe.scenario.draw_wisdom_graph(figsize=(80,80))

# Learning from the same exercises for everybody
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 1, 
#                           number_of_problems_per_givenvars = 1)



# Learning using "moodle random questions" based in a similar level
#pe.challenge_with_randomquestions(max_combinations_givenvars_per_easynesslevel = 2)



# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
pe.exam_with_randomquestions(fill_in_blanks_vars = {'a11', 'a12'}, 
                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
#pe.exploratory() # is the same as
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)



# Teacher can read and choose


#TODO: Dá erro
#pe.hard(max_number_of_problems=10, max_combinations_givenvars_per_easynesslevel=1) # is the same as

#pe.hard(max_number_of_problems=None, 
#        max_combinations_givenvars_per_easynesslevel=None,
#        number_of_problems_per_givenvars=4) # is the same as

#pe.challenge_no_variants(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)
