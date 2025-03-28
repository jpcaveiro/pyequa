
#
# 4 equations (ou generic relations)
#
scenary_relations = {
    "Eq(zobs, qnorm(1-valorp, 0, 1))",    # Equation in R
    "Eq(rejeitarounao, valorp + alpha)",  # Relation 
    "Eq(menormaior, valorp + alpha)",     # Relation
    "Eq(enaoemaior, valorp + alpha)",     # Relation
}


#
# 6 variables: description of each variable controls the way they appear
# 
variable_attributes = {
    'zobs': {'type': float, 'tol': 0.001, 'givenvarlevel': 1},
     #'valorp':  {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
    'valorp':  {'type': str, 'givenvarlevel': 1},
    'alpha':   {'type': str, 'givenvarlevel': 1},
    'rejeitarounao': {'type': str, 'givenvarlevel': 2},
    'menormaior':  {'type': str, 'givenvarlevel': 2},
    'enaoemaior':  {'type': str, 'givenvarlevel': 2},
}

from pathlib import Path
from pyequa.config import PyEqua

PyEqua(Path(__file__).parent).run(scenary_relations, variable_attributes)

