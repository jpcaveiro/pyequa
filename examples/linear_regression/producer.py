# ------------
# linear regression
# Source 1: https://www.perplexity.ai/search/give-an-example-of-linear-regr-5PRl8Iw5RMS.EA5HjOzARQ
# Source 2 (muito a explorar): https://chat.deepseek.com/a/chat/s/af4aaf9c-75bc-466e-9299-ee14de910710
# ------------



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

# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
pe.randomquestion_sameblanks(fill_in_blanks_vars = {'g', 'sqerros', 'sqtotal', 'msqgrupos', 'sig'}, 
                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
#pe.exploratory() # is the same as
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)


# Teacher can read and choose
#pe.hard_first(max_number_of_problems=None, 
#              max_combinations_givenvars_per_easynesslevel=2, 
#              number_of_problems_per_givenvars=1)

