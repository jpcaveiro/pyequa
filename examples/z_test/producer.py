#
# Equations or generic relations
#
scenary_relations = {
    "Eq(zobs, qnorm(1-pvalue, 0, 1))", #equation
    "Eq(reject, pvalue + alpha)", #relation: reject is related with pvalue and alpha
    "Eq(lowergreater, pvalue + alpha)", #relation
    "Eq(sig, pvalue + alpha)", #relation: sig text depends on pvalue and alpha
}


#
# Variables: description of each variable controls the way they appear
# 
variable_attributes = {
    'zobs': {'type': 'numerical', 'tol': 0.001, 'givenvarlevel': 1},
    'pvalue':  {'type': 'multichoice', 'givenvarlevel': 1},
    'alpha':   {'type': 'multichoice', 'givenvarlevel': 1},
    'reject': {'type': 'multichoice', 'givenvarlevel': 2},
    'lowergreater':  {'type': 'multichoice', 'givenvarlevel': 2},
    'sig':  {'type': 'multichoice', 'givenvarlevel': 3},
}

from pyequa.config import PyEqua

pe = PyEqua("z_test", scenary_relations, variable_attributes)



#pe.hard_first(max_number_of_problems=None, 
#              max_combinations_givenvars_per_easynesslevel=5, 
#              number_of_problems_per_givenvars=1)


#pe.randomquestion_sameblanks(fill_in_blanks_vars = {'zobs', 'pvalue', 'reject', 'sig'}, 
#                             number_of_problems_per_givenvars=4)


pe.exploratory() 