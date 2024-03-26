# stats01.py


# %%
#Load wisdomgraph library


#In production use
#import  wisdomgraph as ws

#In development use
import importlib
wisdomgraph = importlib.import_module('wisdomgraph')
importlib.reload(wisdomgraph)
ws = wisdomgraph


# %%
#Ideia

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

# %%
#Texto do cenário

scenary_text = r"""
# essay

Considere a amostra: 

\[
      x_1={x1value}, x_2={x2value}, x_3={x3value}
\]

e a sua média amostral \(\bar x={mediavalue}\) e variância \(s_c^2={varvalue}\).


# question

Determine as incógnitas.

## answer

{answer_steps}
"""


answer_template = """Sabendo

{localinputvars}

e usando

{solvers}

determina-se

{localoutputvars}

"""


# %% 
# Symbols

from sympy import symbols, Eq, Symbol, Rational, latex

#x1,x2,x3,media,variancia = symbols('x1,x2,x3,media,variancia')

x1 = Symbol('x1')
x2 = Symbol('x2')
x3 = Symbol('x3')

media  = Symbol('media')
var    = Symbol('var')


# %%
# Equações

#TODO: apesar do sympy desenhar o latex das equações, essa pode não ser a melhor forma.
#Assim, para cada equação deve haver associada uma string latex que melhor a representa para
#um humano.

eq_media   = Eq(media, Rational(1,3)*(x1+x2+x3))
eq_var     = Eq(var,   Rational(1,3)*( (x1-media)**2 + (x2-media)**2 + (x3-media)**2 ))



#print( ws.SE(Eq(media, Rational(1,3)*(x1+x2+x3))).__repr__() )


#Outra ideia
#scenary = {
#    eq_media: {'symbols': eq_media.free_symbols, 'latex': ''},
#    eq_var: eq_var.free_symbols,
#}



scenary_equations = {
    #ws.SR is class Scenary.SympyRelation (ako "equality")
    ws.SR(eq_media,latex_str="média = (1/3)(x1+x2+x3)"),
    ws.SR(eq_var,  latex_str="variância=(1/3)(x1-média)^2+(x2-média)^2+(x3-média)^2)"),
}





# %%
# wisdomgraph.Scenario(...)

world = wisdomgraph.Scenario(scenary_equations,scenary_text,answer_template,r=[1,2])
#old: sc.build_solvercandidates(r=[1,2])
#old: sc.build_wisdomgraph()

#plot
#world.draw_wisdom_graph(figsize=[80,80])


# %%
# Pequeno teste

world.wisdomgraph.nodes['x1x2']

# %%
#Buildall_exercises(...)


world.buildall_exercises(maxvars=3) #dar ao user 3 variáveis conhecidas



