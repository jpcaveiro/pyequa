

# %% 

import importlib
wisdomgraph = importlib.import_module('wisdomgraph')
importlib.reload(wisdomgraph)

wisdomgraph.Combinations({'a','b','c'})



# %%


import importlib
wisdomgraph = importlib.import_module('wisdomgraph')
importlib.reload(wisdomgraph)



from sympy import symbols

a,b = symbols('a,b')

wisdomgraph.set2strlist({b,a})


# %%
