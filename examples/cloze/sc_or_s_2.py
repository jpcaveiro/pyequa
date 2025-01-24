# sc_or_s.py

"""
Testing moodle cloze quiz construction.

# COMO FAZER ESTAS QUESTÕES com texto

Exemplo:

# Com uma amostra de tamanho [2|4|10|20|100|1000], [pode|deve] ser usado o desvio padrão [corrigido|corrigido ou não]
# pois o desvio padrão corrigido é [maior, ou bastante maior, que o|aproximado ao] desvio padrão não corrigido.

"""

## variante {variation_number}
### feedback


student_template = r"""

O desvio padrão corrigido, \(s_c\), é um estimador centrado para o desvio padrão do modelo populacional \(\sigma\), 
\(E[s_c] = \sigma\).

**(a)** Verifique que para uma amostra de tamanho {tamanhoinput} a relação entre \(s_c\) e \(s\) é dada por:

* \(s_c\) = {racioinput} \(s\)

Apenas para efeitos da próxima alínea, considere, agora, que um racio \(s_c/s\) inferior a 1.01 é negligenciável.

**(b)** Com uma amostra de tamanho {tamanhoinput}, {podedeveinput} ser usado o desvio padrão {corrigidoinput} pois o desvio padrão corrigido é {justificaçãoinput} desvio padrão não corrigido.

Avalie a qualidade deste exercício para o estudo: {{:MULTICHOICE:=útil\~%100%não útil\~%100%não compreendo\~%100%acho que não tem solução}}.

"""

student_feedback = r"""

#(Consulte o docente das suas turmas ou uma OT.)

"""


# COMO FAZER ESTAS QUESTÕES:

# Com uma amostra de tamanho {tamanhoinput}, [pode|deve] ser usado o desvio padrão [corrigido|corrigido ou não]
# pois o desvio padrão corrigido é [maior, ou bastante maior, que o|aproximado ao] desvio padrão não corrigido.



#import os
#os.chdir(r"C:\Users\pedrocruz\Documents\+Outros\WorkPackages\2024-pyequa\2-trig-c1")


from sympy import symbols, Eq, Symbol #, Rational, latex



n = Symbol('n')
tamanho = Symbol('tamanho')
racio = Symbol('racio')
podedeve = Symbol('podedeve')
corrigido = Symbol('corrigido')
justificação = Symbol('justificação')


# %%
# Equações

#from sympy import FiniteSet, Eq
#s = FiniteSet(1, 2, 3, 4)
#print(s)  # Output: {1, 2, 3, 4}

# Relações:
#
#     tamanho   <1:1> racio
#     tamanho   <n:1> justificação
#     podedeve  <1:1> justificação
#     corrigido <1:1> justificação
#
# Como representar estas relações? A relação está imposta
# no ficheiro Excel.
#
# Bizarro mas é para desenrascar.
def_1  = Eq(n,tamanho)
def_2  = Eq(tamanho, n)
def_3  = Eq(podedeve, n) 
def_4  = Eq(corrigido, n)
def_5  = Eq(racio,n)
def_6  = Eq(justificação,n) 




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
    ws.SR(def_4, latex_str=str(def_4)),
    ws.SR(def_5, latex_str=str(def_5)),
    ws.SR(def_6, latex_str=str(def_6)),
}


# Choose where to store this exercise
from os import getcwd, chdir
print(f"Current: {getcwd()}")
chdir(r"examples/cloze")
print(f"Current: {getcwd()}")


text_service = ClozeService(
                 student_template=student_template, 
                 student_feedback=student_feedback, 
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
#Buildall(...)

#all_paths = world.buildall(no_of_given_vars=2) 
all_paths = world.buildall(no_of_given_vars=None) #increased difficult ?


