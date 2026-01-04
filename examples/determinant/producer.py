# --------------------------
# determinant
# --------------------------


#
# Equations or generic relations
#
scenario_relations = {
    "Eq(d, a11*a22 - a12*a21)",
    "Eq(uniquesolution, d)",
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
    'uniquesolution': {'type': 'multichoice',  'givenvarlevel': 2},
}


from pyequa.config import PyEqua

pe = PyEqua("determinant", scenario_relations, variable_attributes)


#pe.randomquestion_sameblanks(fill_in_blanks_vars = {'a11', 'a12'}, 
#                             number_of_problems_per_givenvars=4)

pe.exploratory()

#pe.hard_first() 
