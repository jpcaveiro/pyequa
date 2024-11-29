# sc_or_s.py

"""
Testing moodle cloze quiz construction.

# COMO FAZER ESTAS QUESTÕES com texto

Exemplo:

# Com uma amostra de tamanho [2|4|10|20|100|1000], [pode|deve] ser usado o desvio padrão [corrigido|corrigido ou não]
# pois o desvio padrão corrigido é [maior, ou bastante maior, que o|aproximado ao] desvio padrão não corrigido.

"""

student_template = r"""
## variante {variation_number}

O desvio padrão corrigido é um estimador centrado para o desvio padrão do modelo populacional \(\sigma^2\).

**(a)** Justifique que \(s_c^2\) é estritamente maior que \(s^2\) mas nem sempre "muito maior".

**(b)** Com uma amostra de tamanho {tamanhoinput}, {podedeveinput} ser usado o desvio padrão {corrigidoinput} 
pois o desvio padrão corrigido é {justificaçãoinput} desvio padrão não corrigido.

Qualidade deste exercício para o estudo: {{:MULTICHOICE:=útil\~%100%não útil\~%100%não compreendo\~%100%acho que não tem solução}}.


### feedback

(Consulte o docente das suas turmas ou uma OT.)

"""

# COMO FAZER ESTAS QUESTÕES:

# Com uma amostra de tamanho {tamanhoinput}, [pode|deve] ser usado o desvio padrão [corrigido|corrigido ou não]
# pois o desvio padrão corrigido é [maior, ou bastante maior, que o|aproximado ao] desvio padrão não corrigido.



#import os
#os.chdir(r"C:\Users\pedrocruz\Documents\+Outros\WorkPackages\2024-pyequa\2-trig-c1")


from sympy import symbols, Eq, Symbol #, Rational, latex



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
def_1  = Eq(tamanho, podedeve+corrigido)
def_2  = Eq(tamanho, corrigido+justificação) #estas são proposições "equivalentes"
def_3  = Eq(tamanho, justificação) #estas são proposições "equivalentes"
#Ver em baixo também vvvvv


# ----------------------
# Call pyequa API
# ----------------------

from pyequa import wisdomgraph as ws
from pyequa.servicecloze import ClozeService

scenary_relations = {
    #ws.SR is class Scenary.SympyRelation (ako "equality")
    ws.SR(def_1, latex_str=str(def_1)),
    ws.SR(def_2, latex_str=str(def_2)),
    ws.SR(def_3, latex_str=str(def_3)),
}


# Choose where to store this exercise
from os import getcwd, chdir
print(f"Current: {getcwd()}")
chdir(r"examples/cloze")
print(f"Current: {getcwd()}")


text_service = ClozeService(
                 student_template=student_template, 
                 excel_pathname="sc_or_s.xlsx",
                 author="Pedro Cruz",
                 sequencial=True,
                 varcount=1)


#world = ws.Scenario(scenary_relations, text_service,r=[2])
world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]


#plot
#world.draw_wisdom_graph(figsize=[80,80])


# %%
# Pequeno teste

#world.wisdomgraph.nodes['ab']
#world.wisdomgraph.nodes['abdx']

# %%
#Buildall_exercises(...)

#all_paths = world.buildall_exercises(no_of_given_vars=2) 
all_paths = world.buildall_exercises(no_of_given_vars=None) #increased difficult ?


