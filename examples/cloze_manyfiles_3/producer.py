
#
# Equations or generic relations
#
scenary_relations = {
    "Eq(disty, ndiassemana+probsucesso)",                 
    "Eq(probvalory, ndiassemana+probsucesso+valory)",     
    "Eq(probsemanas, ndiassemana+probsucesso+nsemanas)",  
}


#
# 6 variables: description of each variable controls the way they appear
# 
variable_attributes = {
    'ndiassemana': {'type': 'numerical',   'tol': 0, 'givenvarlevel': 1},
    'valory':      {'type': 'numerical',   'tol': 0, 'givenvarlevel': 1},
    'probsucesso': {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 1},
    'nsemanas':    {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1},
    'disty':       {'type': 'multichoice', 'givenvarlevel': 2},
    'probvalory':  {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 2},
    'probsemanas': {'type': 'numerical', 'tol': 0.05, 'givenvarlevel': 2},
}

# Not all discounts
# https://docs.moodle.org/405/en/Import_questions
# minus or plus from
#    100, 90, 80, 75, 70, 66.666, 60, 50, 40, 33.333, 30, 25, 20, 16.666, 14.2857, 12.5, 11.111, 10, 5, 0
distractors = {
  'disty': {'disty_d1': '-33.333', 'disty_d2': '-33.333', 'disty_d3': '-33.333'},
  'nembalagens': None,
}



from pathlib import Path
from pyequa.config import PyEqua

PyEqua(Path(__file__).parent).run(scenary_relations, variable_attributes, distractors)

