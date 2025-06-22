
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
#world.buildall(no_of_given_vars=None, max_ex_per_comb=3) 



from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenario_relations, variable_attributes)

# Learning from the same exercises for everybody
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 2, 
#                           number_of_problems_per_givenvars = 4,
#)


# Learning using "moodle random questions" based in a similar level
#pe.challenge_with_randomquestions(max_combinations_givenvars_per_easynesslevel = 2)



# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
#pe.randomquestion_sameblanks(fill_in_blanks_vars = {'probvalory', 'probsemanas'}, 
#                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
#pe.exploratory() # is the same as
#pe.challenge_no_variants(max_combinations_givenvars_per_easynesslevel = None,  # no control
#                         number_of_problems_per_givenvars = 1,  # single variant for each case
#)



# Teacher can read and choose
pe.hard(max_number_of_problems=4, max_combinations_givenvars_per_easynesslevel=None) # is the same as

#pe.scenario.draw_wisdom_graph(figsize=[100,100])


