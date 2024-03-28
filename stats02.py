# stats02.py


# %%


#Production
#import  wisdomgraph as ws

#Development
import importlib
wisdomgraph = importlib.import_module('wisdomgraph')
importlib.reload(wisdomgraph)
ws = wisdomgraph



# Symbol

from sympy import Eq, Symbol, Rational

#x1,x2,x3,media,variancia = symbols('x1,x2,x3,media,variancia')

# Y = beta0 + beta1 x + epsilon


b0 = Symbol("b0")
b1 = Symbol("b1")

sx = Symbol('sx')
sy = Symbol('sy')
sxx = Symbol('sxx')
#syy = Symbol('syy')
sxy = Symbol('sxy')

nv  = Symbol('nv')


# Equações

eq_beta0 = Eq(b0, (sy*sxx-sx*sxy)/(nv*sxx-sx*sx))
eq_beta1 = Eq(b1, (nv*sxy-sx*sy)/(nv*sxx-sx*sx))


scenary_equations = {
    ws.SR(eq_beta0,latex_str="b0 = (sy*sxx-sx*sxy)/(nv*sxx-sx*sx)"),
    ws.SR(eq_beta1,latex_str="b1 = (nv*sxy-sx*sy)/(nv*sxx-sx*sx)"),
}



# removido
# * \(\sum Y_i^2\) = {syyvalue}


scenary_text = r"""
# essay

Uma pesquisa com \(n\) = {nvvalue} estudantes de ISCED-Cabinda obteve os seguintes resultados sobre a relação linear

\(Y = \beta_0 + \beta_1 x + \epsilon\)

entre horas de estudo por semana \(x\) e nota final na disciplina \(Y\):

* \(\beta_0\) = {b0value}
* \(\beta_1\) = {b1value}
* \(n\) = {nvvalue}
* \(\sum x_i\) = {sxvalue}
* \(\sum Y_i\) = {syvalue}
* \(\sum x_i^2\) = {sxxvalue}
* \(\sum x_i Y_i\) = {sxyvalue}


# question

Determine as incónitas.

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
# wisdomgraph.Scenario(...)

world = wisdomgraph.Scenario(scenary_equations,scenary_text,answer_template,r=[1,2])

#plot
#world.draw_wisdom_graph(figsize=[80,80])


# %%
# Pequeno teste

world.wisdomgraph.nodes['b0b1']

# %%
#Buildall_exercises(...)


world.buildall_exercises(maxvars=6) #dar ao user maxvar variáveis conhecidas


# %%
#VER estes casos


# Com 
#    world.buildall_exercises(maxvars=6) 
# surge o exempo abaixo mas também há uma situação de erro porque ## answer fica vazio!

r"""
# essay

Uma pesquisa com \(n\) = um valor estudantes de ISCED-Cabinda obteve os seguintes resultados sobre a relação linear

\(Y = \beta_0 + \beta_1 x + \epsilon\)

entre horas de estudo por semana \(x\) e nota final na disciplina \(Y\):

* \(\beta_0\) = um valor
* \(\beta_1\) = um valor
* \(n\) = um valor
* \(\sum x_i\) = um valor
* \(\sum Y_i\) = um valor
* \(\sum x_i^2\) = incónita
* \(\sum x_i Y_i\) = incónita


# question

Determine as incónitas.

## answer

Sabendo

{nv, sx, b0, sy, b1}

e usando

b0 = (sy*sxx-sx*sxy)/(nv*sxx-sx*sx)

b1 = (nv*sxy-sx*sy)/(nv*sxx-sx*sx)

determina-se

{sxx, sxy}
"""

