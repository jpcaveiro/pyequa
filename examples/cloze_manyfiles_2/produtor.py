


scenary_relations = {
    "Eq(zobs, qnorm(1-valorp, 0, 1))",
    "Eq(rejeitarounao, valorp + alpha)",
    "Eq(menormaior, valorp + alpha)",
    "Eq(enaoemaior, valorp + alpha)",
}



#TODO: 
# Ver "TODO" no ficheiro: 
#  C:\Users\pedrocruz\Documents\GitHub\pyequa\examples\cloze_manyfiles\produtor.py
#
variable_attributes = {
    'zobs': {'type': float, 'tol': 0.001, 'givenvarlevel': 1},
    #'valorp':  {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
    'valorp':  {'type': str, 'givenvarlevel': 1},
    'alpha':   {'type': str, 'givenvarlevel': 1},
    'rejeitarounao': {'type': str, 'givenvarlevel': 2},
    'menormaior':  {'type': str, 'givenvarlevel': 2},
    'enaoemaior':  {'type': str, 'givenvarlevel': 2},
}



student_feedback = r"""

(Consulte o docente das suas turmas ou uma OT.)

"""


from pyequa import wisdomgraph as ws
from pyequa.servicecloze import ClozeService


# Choose where to store this exercise
from os import getcwd, chdir
print(f"Current file:\n{getcwd()}")
chdir(r"examples\\cloze_manyfiles_2")
print(f"Current: {getcwd()}")


text_service = ClozeService(
                 student_template="enunciado.md", 
                 student_feedback=student_feedback, 
                 excel_pathname="dados.xlsx",
                 variable_attributes=variable_attributes,
                 author="Pedro Cruz",
                 sequencial=True,
                 varcount=1)


#world = ws.Scenario(scenary_relations, text_service,r=[2])
world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]

#examples
#world.buildall(no_of_given_vars=2, max_ex_per_comb=10) 


#increased difficult no_of_given_vars=None
world.buildall(no_of_given_vars=None, max_ex_per_comb=3) 



