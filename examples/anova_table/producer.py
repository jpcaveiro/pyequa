# ------------
# anova_table
# ------------


#
# Equations or generic relations
#
scenario_relations = {
    "Eq(dfgroups,  g-1)",
    "Eq(dferrors,  g*n-g)",
    "Eq(sqtotal,   sqgroups+sqerrors)",
    "Eq(dftotal,   dfgroups+dferrors)",
    "Eq(msqgroups, sqgroups/dfgroups)",
    "Eq(msqerrors, sqerrors/dferrors)",
    "Eq(f,         msqgroups/msqerrors)",
    "Eq(sig,       f)",  # means sig and f are related
    "Eq(rejecth0, sig)", # means sig will define rejection of H0
}

#
# Variables: description of each variable controls the way they appear
# 
variable_attributes = {
    'g': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'n': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'sqgroups': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'sqerrors': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 1},
    'sqtotal': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'dfgroups': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'dferrors': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
    'dftotal': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 2},
    'msqgroups': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'msqerrors': {'type': 'numerical', 'tol': 0.05,  'givenvarlevel': 2},
    'f': {'type': 'numerical', 'tol': 0.005,  'givenvarlevel': 3},
    'sig': {'type': 'numerical', 'tol': 0.005,  'givenvarlevel': 3},
    'rejecth0': {'type': 'multichoice', 'givenvarlevel': 3},
}


from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

#pe.scenario.draw_wisdom_graph()

# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
pe.randomquestion_sameblanks(fill_in_blanks_vars = {'sqtotal', 'msqgrupos', 'sig', 'rejecth0'}, 
                             number_of_problems_per_givenvars=1)



# Teacher can read and choose
#pe.exploratory() 


# Teacher can read and choose
#pe.hard_first(max_number_of_problems=None, 
#              max_combinations_givenvars_per_easynesslevel=5, 
#              number_of_problems_per_givenvars=1)

