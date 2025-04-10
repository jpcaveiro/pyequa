
#
# Equations or generic relations
#
scenario_relations = {
    "Eq(disty, ndiassemana+probsucesso)",                 
    "Eq(probvalory, ndiassemana+probsucesso+valory)",     
    "Eq(probsemanas, ndiassemana+probsucesso+nsemanas)",  
}


#
# 6 variables: description of each variable controls the way they appear
# 
variable_attributes = {
    # Inteiros
    'ndiassemana': {'type': 'numerical', 'tol': 0,    'givenvarlevel': 1},
    'valory':      {'type': 'numerical', 'tol': 0,    'givenvarlevel': 1},
    'nsemanas':    {'type': 'numerical', 'tol': 0,    'givenvarlevel': 1},
    # Reais
    'probsucesso': {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 1},
    'probvalory':  {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 2},
    'probsemanas': {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 2},
    # Multichoice com distratores
    'disty':       {'type': 'multichoice',            'givenvarlevel': 2, 
                    'distractors': {'disty_d1': '-33.333', 'disty_d2': '-33.333', 'disty_d3': '-33.333'}},
    # Distratora pura (não é variável de interesse ao problema)
    'nembalagens': {'type': 'distractor'},
}


# MOODLE: Not all discounts
# https://docs.moodle.org/405/en/Import_questions
# minus or plus from
#    100, 90, 80, 75, 70, 66.666, 60, 50, 40, 33.333, 30, 25, 20, 16.666, 14.2857, 12.5, 11.111, 10, 5, 0


from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

# Learning from the same exercises for everybody
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 2, 
#                           number_of_problems_per_givenvars = 4,
#)


# Learning using "moodle random questions" based in a similar level
#pe.challenge_with_randomquestions(max_combinations_givenvars_per_easynesslevel = 2)



# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
#pe.exam_with_randomquestions(fill_in_blanks_vars = {'probvalory', 'probsemanas'}, 
#                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
#pe.exploratory() # is the same as
#pe.challenge_no_variants(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)



# Teacher can read and choose
#pe.hard(requested_number_of_problems=4, max_combinations_givenvars_per_easynesslevel=1) # is the same as
#pe.challenge_no_variants(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)

pe.scenario.draw_wisdom_graph(figsize=[100,100])

