# trig.py

"""
Trigonometrical relations.
"""



from pyequa import wisdomgraph as ws
from pyequa.serviceabstract import TextService

from sympy import symbols, Eq, Symbol, Rational, latex
from sympy import sin, cos, csc, cot


student_template = r"""
# essay

Sabendo que 

* $x$ é um valor real 
* $a=\sin(x)$ 
* $b=\cos(x)$ 
* $c=\text{{cossec}}(x)$ 
* $d=\text{{cotan}}(x)$

determine as incógnitas

* \(a\) = {ainput}
* \(b\) = {binput}
* \(c\) = {cinput}
* \(d\) = {dinput}
* \(x\) = {xinput}

"""


teacher_template = r"""
# essay

Sabendo que 

* $x$ é um valor real 
* $a=\sin(x)$
* $b=\cos(x)$
* $c=\text{{cossec}}(x)$ 
* $d=\text{{cotan}}(x)$

determine as incógnitas

* \(a\) = {ainput} = {aoutput}
* \(b\) = {binput} = {boutput}
* \(c\) = {cinput} = {coutput}
* \(d\) = {dinput} = {doutput}
* \(x\) = {xinput} = {xoutput}


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

#import os
#os.chdir(r"C:\Users\pedrocruz\Documents\+Outros\WorkPackages\2024-pyequa\2-trig-c1")



x = Symbol('x')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')


# %%
# Equações

#TODO: apesar do sympy desenhar o latex das equações, essa pode não ser a melhor forma.
#Assim, para cada equação deve haver associada uma string latex que melhor a representa para
#um humano.

def_1  = Eq(a, sin(x))
def_2  = Eq(b, cos(x))
def_3  = Eq(c, csc(x))
def_4  = Eq(d, cot(x))
eq_1   = Eq(1, a**2 + b**2)
eq_2   = Eq(1/a, c )
eq_3   = Eq(d**2, c**2 - 1 )



scenary_relations = {
    #ws.SR is class Scenary.SympyRelation (ako "equality")
    ws.SR(def_1, latex_str=str(def_1)),
    ws.SR(def_2, latex_str=str(def_2)),
    ws.SR(def_3, latex_str=str(def_3)),
    ws.SR(def_4, latex_str=str(def_4)),
    ws.SR(eq_1, latex_str="sin^2+cos^2=1"),
    ws.SR(eq_2, latex_str="1/sin = cosec"),
    ws.SR(eq_3, latex_str="cotan^2 = cosec^2 - 1"),
}




text_service = TextService(
                 student_template, 
                 teacher_template, 
                 answer_template, 
                 excel_pathname="trig.xlsx",
                 basename="trig",
                 extension="Rmd",
                 all_ex_in_samefile=True,
                 varcount=2,
                 cloze_type=True) #moodle style (type="Rmd")




world = ws.Scenario(scenary_relations,
                    text_service,
                    r=[1,2])


#plot
world.draw_wisdom_graph(figsize=[80,80])


# %%
# Pequeno teste

#world.wisdomgraph.nodes['ab']

#world.wisdomgraph.nodes['abdx']


# %%
#Buildall_exercises(...)


#dar ao user 3 variáveis conhecidas
all_paths = world.buildall_exercises(maxvars=2) 


