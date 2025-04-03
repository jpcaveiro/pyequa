
#
# 4 equações (ou relações)
#
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

# 6 variáveis
variable_attributes = {
    'zobs': {'type': float, 'tol': 0.001, 'givenvarlevel': 1},
    #'valorp':  {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
    'valorp':  {'type': str, 'givenvarlevel': 1},
    'alpha':   {'type': str, 'givenvarlevel': 1},
    'rejeitarounao': {'type': str, 'givenvarlevel': 2},
    'menormaior':  {'type': str, 'givenvarlevel': 2},
    'enaoemaior':  {'type': str, 'givenvarlevel': 2},
}


# com 4 equações, em geral, consegue-se 4 variáveis
# exemplo: sistema de 4 equações a 4 incógnitas


import os
from pathlib import Path

# Path to the default configuration file
from pyequa.config import get_config
CONFIG_PATH = Path(__file__).parent / "config.yaml"
config = get_config(CONFIG_PATH)


from pyequa import scenario as ws
from pyequa.servicecloze import ClozeService


# Choose where to store this exercise
#from os import getcwd, chdir
#print(f"Current file:\n{getcwd()}")
#chdir(r"examples\\cloze_manyfiles_2")
#print(f"Current: {getcwd()}")


pandas_dataframe = pd.read_excel("dados.xlsx")


text_service = ClozeService(
                 student_template="enunciado.md", 
                 student_feedback=student_feedback, 
                 pandas_dataframe=pandas_dataframe,
                 variable_attributes=variable_attributes,
                 author="Pedro Cruz",
                 sequencial=True,
                 output_extension='md',
                 varcount=1)


#world = ws.Scenario(scenary_relations, text_service,r=[2])
world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]

# Individual examples
#world.buildall(no_of_given_vars=1, max_ex_per_comb=10) 


# Increased difficult no_of_given_vars=None
world.buildall(no_of_given_vars=None, max_ex_per_comb=3) 



