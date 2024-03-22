# stats01.py


# %%


#Production
#import  wisdomgraph as ws

#Development
import importlib
wisdomgraph = importlib.import_module('wisdomgraph')
importlib.reload(wisdomgraph)
ws = wisdomgraph



"""

Equações:

media = (1/3)*(x1+x2+x3)
var = (1/3)*( (x1-media)^2 + (x2-media)^2 + (x3-media)^3 )

Objetivo:

Sabendo que numa amostra de dimensão 3 se tem


x1 = 5
x2 = 10
media = 3.4

Determine:

var = ?
x3?
"""


scenary_tex = r"""
# essay

Considere a amostra: 

\[
      {x1}, {x2}, {x3}
\]

e a sua média amostral \(media\) e variância \(variancia\).


# question

Determine {{outputvars}}.

## answer

{{answer}}

"""



# Symbol

from sympy import symbols, Eq, Symbol, Rational, latex

#x1,x2,x3,media,variancia = symbols('x1,x2,x3,media,variancia')

x1 = Symbol('x_1')
x2 = Symbol('x_2')
x3 = Symbol('x_3')

media     = Symbol(r'\bar{x}')
variancia = Symbol(r's_c^2')



# Equações
#TODO: apesar do sympy desenhar o latex das equações, essa pode não ser a melhor forma.
#Assim, para cada equação deve haver associada uma string latex que melhor a representa para
#um humano.

eq_media   = Eq(media, Rational(1,3)*(x1+x2+x3))
eq_var     = Eq(variancia, Rational(1,3)*( (x1-media)**2 + (x2-media)**2 + (x3-media)**3 ))



#print( ws.SE(Eq(media, Rational(1,3)*(x1+x2+x3))).__repr__() )


#scenary = {
#    eq_media: {'symbols': eq_media.free_symbols, 'latex': ''},
#    eq_var: eq_var.free_symbols,
#}

scenary = {
    ws.SR(eq_media,latex_str="média = (1/3)(x1+x2+x3)"),
    ws.SR(eq_var,  latex_str="variância=(1/3)(x1-média)^2+(x2-média)^2+(x3-média)^2)"),
}





'''

def mk_output_vars_str(outputvars):
    """
    input:

    - outputvars: sympy symbols

    output:

    - a str

    """

    vlist = [latex(s) for s in outputvars]
    vstr = ', '.join(sorted(vlist))
    return vstr

print(mk_output_vars_str({x1,x2,media}))
'''







world = wisdomgraph.Scenario(scenary,r=[1,2],scenary_tex=scenary_tex)
#old: sc.build_solvercandidates(r=[1,2])
#old: sc.build_wisdomgraph()

#plot
#world.draw_wisdom_graph(figsize=[80,80])



print(world.combine_and_mk_exercises(3))


# ONDE VOU:
# Usar SympyRelation para ajudar a preencher `scenary_tex` acima.


# %%

world.wisdomgraph.nodes['x_1x_2']

# %%
