# --------------------------
# cloze_manyfiles_5_tabela
# --------------------------

from pathlib import Path
exercise_folder = Path(__file__).parent
print(exercise_folder)
import os
os.chdir(exercise_folder)

#
# Equations or generic relations
#
scenario_relations = {
    "Eq(dfgrupos,  g-1)",
    "Eq(dferros,   g*n-g)",
    "Eq(sqtotal,   sqgrupos+sqerros)",
    "Eq(dftotal,   dfgrupos+dferros)",
    "Eq(msqgrupos, sqgrupos/dfgrupos)",
    "Eq(msqerros,  sqerros/dferros)",
    "Eq(f,         msqgrupos/msqerros)",
    "Eq(sig,       f)",
    "Eq(rejeitarh0, sig)",
}

#
# Variables: description of each variable controls the way they appear
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
    'f': {'type': 'numerical', 'tol': 0.005,  'givenvarlevel': 3},
    'sig': {'type': 'numerical', 'tol': 0.005,  'givenvarlevel': 3},
    'rejeitarh0': {'type': 'multichoice', 'givenvarlevel': 3},
}


from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

#pe.scenario.draw_wisdom_graph()


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
