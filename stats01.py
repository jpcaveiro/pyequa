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



# %% 
# Symbols

from sympy import symbols, Eq, Symbol, Rational, latex

#x1,x2,x3,media,variancia = symbols('x1,x2,x3,media,variancia')

x1 = Symbol('x_1')
x2 = Symbol('x_2')
x3 = Symbol('x_3')

media     = Symbol(r'\bar{x}')
variancia = Symbol(r's_c^2')


# %%
# Equações

#TODO: apesar do sympy desenhar o latex das equações, essa pode não ser a melhor forma.
#Assim, para cada equação deve haver associada uma string latex que melhor a representa para
#um humano.

eq_media   = Eq(media, Rational(1,3)*(x1+x2+x3))
eq_var     = Eq(variancia, Rational(1,3)*( (x1-media)**2 + (x2-media)**2 + (x3-media)**2 ))



#print( ws.SE(Eq(media, Rational(1,3)*(x1+x2+x3))).__repr__() )


#scenary = {
#    eq_media: {'symbols': eq_media.free_symbols, 'latex': ''},
#    eq_var: eq_var.free_symbols,
#}

scenary = {
    ws.SR(eq_media,latex_str="média = (1/3)(x1+x2+x3)"),
    ws.SR(eq_var,  latex_str="variância=(1/3)(x1-média)^2+(x2-média)^2+(x3-média)^2)"),
}





# %%
# wisdomgraph.Scenario(...)

world = wisdomgraph.Scenario(scenary,r=[1,2])
#old: sc.build_solvercandidates(r=[1,2])
#old: sc.build_wisdomgraph()

#plot
#world.draw_wisdom_graph(figsize=[80,80])


# %%
# Pequeno teste

world.wisdomgraph.nodes['x_1x_2']

# %%
#Buildall_exercises(...)


def author_scenary_text(inputvars_set,outputvars_set,solverslist_text):
    """
    - inputvars_set
    - outputvars_set
    - solvers_list
    """
    
    
    text = r"""
# essay

Considere a amostra: 

\[
      x_1={x1value}, x_2={x2value}, x_3={x3value}
\]

e a sua média amostral \(\bar x={mediavalue}\) e variância \(s_c^2={varianciavalue}\).


# question

Determine as incógnitas.

## answer

{answer_steps}

    """

    VALOR = "um valor"
    UNKNOWN = "incónita"

    x1value = VALOR if x1 in inputvars_set else UNKNOWN
    x2value = VALOR if x2 in inputvars_set else UNKNOWN
    x3value = VALOR if x3 in inputvars_set else UNKNOWN

    mediavalue = VALOR if media in inputvars_set else UNKNOWN
    varianciavalue = VALOR if variancia in inputvars_set else UNKNOWN




    print(text.format(
        x1value = x1value,
        x2value = x2value,
        x3value = x3value,
        mediavalue = mediavalue,
        varianciavalue = varianciavalue,
        answer_steps = solverslist_text,
    ))



world.buildall_exercises(author_scenary_text,maxvars=3)

# %%
