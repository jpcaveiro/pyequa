# sc_or_s.py

"""
Testing moodle cloze quiz construction.
"""

from os import getcwd, chdir
print(f"Current: {getcwd()}")
chdir(r"examples/cloze")
print(f"Current: {getcwd()}")



from pyequa import wisdomgraph as ws
from pyequa.textservice import TextService

from sympy import symbols, Eq, Symbol #, Rational, latex


student_template = r"""
## variante {variation_number}


Com uma amostra de tamanho {tamanhoinput}, {s_or_scinput} pois {justificaçãoinput}.

### feedback

(Consulte o docente das suas turmas ou uma OT.)

Com uma amostra de tamanho {tamanhooutput}, "{s_or_scoutput}" pois "{justificaçãooutput}".

"""


teacher_template = r"""
## variante {variation_number}


Com uma amostra de tamanho {tamanhoinput}, {s_or_scinput} pois {justificaçãoinput}.

Com uma amostra de tamanho {tamanhooutput}, "{s_or_scoutput}" pois "{justificaçãooutput}".

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



tamanho = Symbol('tamanho')
s_or_sc = Symbol('s_or_sc')
justificação = Symbol('justificação')


# %%
# Equações


# Relações:
#
#     tamanho <-n:1-> s_or_sc <-1:1-> justificação
#
# Como representar estas relações? A relação está imposta
# no ficheiro Excel.
#
# Bizarro mas é para desenrascar.
def_1  = Eq(tamanho, s_or_sc)
def_2  = Eq(s_or_sc, justificação) #estas são proposições "equivalentes"


scenary_relations = {
    #ws.SR is class Scenary.SympyRelation (ako "equality")
    ws.SR(def_1, latex_str=str(def_1)),
    ws.SR(def_2, latex_str=str(def_2)),
}




text_service = TextService(
                 student_template, 
                 teacher_template, 
                 answer_template, 
                 excel_pathname="sc_or_s.xlsx",
                 basename="sc_or_s",
                 extension="Rmd",
                 all_ex_in_samefile=True,
                 varcount=2,  #TODO: como garantir que cada estudante ao aprender vê um caso diferente?
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
all_paths = world.buildall_exercises(no_of_given_vars=2) 


