
scenary_relations = {
    "Eq(probB, CDF_Binom(valorx,n,probacerto))",
    "Eq(medianormal, n * probacerto)",
    "Eq(varnormal, n * probacerto * (1-probacerto))",
    "Eq(probN, CDF_Normal(valorx,medianormal,sqrt(varnormal)))",
    "Eq(verificamedia, n * probacerto >= 5)",
    "Eq(verificavar, n * probacerto * (1-probacerto) >= 5)",
    "Eq(verifican, n >= 30)",
}


#TODO: por implementar:
# 1. tol como este método e com excel
# 2. prioridade das variáveis "dadas" sobre as "output" naturais
# 3. Como obter relações a partir das equações acima? Produzir um ficheiro a ser preenchido depois da consulta aos dados do Excel?
variable_attributes = {
    'n': {'type': int, 'tol': 0, 'givenvarlevel': 1},
    'probacerto':  {'type': float, 'tol': 0.001, 'givenvarlevel': 1},
    'valorx': {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
    'probB':  {'type': float, 'tol': 0.001, 'givenvarlevel': 2},
    'medianormal':  {'type': float, 'tol': 0.001, 'givenvarlevel': 3},
    'varnormal':  {'type': float, 'tol': 0.001, 'givenvarlevel': 3},
    'probN':  {'type': float, 'tol': 0.001, 'givenvarlevel': 4},
    'verificamedia':  {'type': str, 'givenvarlevel': 4},
    'verificavar':  {'type': str, 'givenvarlevel': 4},
    'verifican':  {'type': str, 'givenvarlevel': 4},
}



student_feedback = r"""

#(Consulte o docente das suas turmas ou uma OT.)

"""

from pyequa import scenario as ws
from pyequa.servicecloze import ClozeService


# Choose where to store this exercise
from os import getcwd, chdir
print(f"Current file:\n{getcwd()}")
chdir(r"examples/cloze_manyfiles")
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
#TODO: repensar r=[1,2]: talvez logo r=[1,2,3,...,oo[ até não existir caminho ?
world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]

all_paths = world.buildall(no_of_given_vars=4, max_ex_per_comb=10) #increased difficult ?