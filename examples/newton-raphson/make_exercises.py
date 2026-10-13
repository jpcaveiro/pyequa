from pyequa.config import PyEqua
from pathlib import Path


variable_attributes = {
    'FUN': {'type': 'multichoice', 'givenvarlevel': 1},
    'ALPHA': {'type': 'numerical', 'tol': 0.0001, 'givenvarlevel': 3},
    'X0': {'type': 'numerical', 'tol': 0.0001, 'givenvarlevel': 1},
    'X1': {'type': 'numerical', 'tol': 0.0001, 'givenvarlevel': 2},
    'X2': {'type': 'numerical', 'tol': 0.0001, 'givenvarlevel': 3},
    'ERRABS': {'type': 'numerical', 'tol': 0.0001, 'givenvarlevel': 3},
    'A': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1},
    'B': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1},
}

scenario_relations = {
   'Eq(FUN,A+B)',
   'Eq(X1, X0)',
   'Eq(X2, X1)',
   'Eq(X2, X1)',
   'Eq(ERRABS, ALPHA+X2)',
}

pe = PyEqua(Path('newton-raphson'), scenario_relations, variable_attributes)



import warnings
warnings.filterwarnings("error", category=SyntaxWarning)

pe.randomquestion_sameblanks(
    fill_in_blanks_vars = {
        'X0'
    },
    number_of_problems_per_givenvars=None) #None means all in data file

