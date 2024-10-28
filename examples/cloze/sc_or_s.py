# sc_or_s.py

"""
Testing moodle cloze quiz construction.

# COMO FAZER ESTAS QUESTÕES com texto

Exemplo:

# Com uma amostra de tamanho [2|4|10|20|100|1000], [pode|deve] ser usado o desvio padrão [corrigido|corrigido ou não]
# pois o desvio padrão corrigido é [maior, ou bastante maior, que o|aproximado ao] desvio padrão não corrigido.

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

O desvio padrão corrigido é um estimador centrado para o desvio padrão do modelo populacional.

Com uma amostra de tamanho {tamanhoinput}, {podedeveinput} ser usado o desvio padrão {corrigidoinput} 
pois o desvio padrão corrigido é {justificaçãoinput} desvio padrão não corrigido.

### feedback

(Consulte o docente das suas turmas ou uma OT.)

"""

# COMO FAZER ESTAS QUESTÕES:

# Com uma amostra de tamanho {tamanhoinput}, [pode|deve] ser usado o desvio padrão [corrigido|corrigido ou não]
# pois o desvio padrão corrigido é [maior, ou bastante maior, que o|aproximado ao] desvio padrão não corrigido.


teacher_template = r"""
## variante {variation_number}

O desvio padrão corrigido é um estimador centrado para o desvio padrão do modelo populacional.

Com uma amostra de tamanho {tamanhoinput}, {podedeveinput} ser usado o desvio padrão {corrigidoinput} 
pois o desvio padrão corrigido é {justificaçãoinput} desvio padrão não corrigido.

## answer

Com uma amostra de tamanho {tamanhooutput}, {podedeveoutput} ser usado o desvio padrão {corrigidooutput} 
pois o desvio padrão corrigido é {justificaçãooutput} desvio padrão não corrigido.


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
podedeve = Symbol('podedeve')
corrigido = Symbol('corrigido')
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
def_1  = Eq(tamanho, podedeve)
def_2  = Eq(podedeve, corrigido) #estas são proposições "equivalentes"
def_3  = Eq(corrigido, justificação) #estas são proposições "equivalentes"


scenary_relations = {
    #ws.SR is class Scenary.SympyRelation (ako "equality")
    ws.SR(def_1, latex_str=str(def_1)),
    ws.SR(def_2, latex_str=str(def_2)),
    ws.SR(def_3, latex_str=str(def_3)),
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
#world.draw_wisdom_graph(figsize=[80,80])


# %%
# Pequeno teste

#world.wisdomgraph.nodes['ab']

#world.wisdomgraph.nodes['abdx']


# %%
#Buildall_exercises(...)


#dar ao user 3 variáveis conhecidas
all_paths = world.buildall_exercises(no_of_given_vars=2) 


