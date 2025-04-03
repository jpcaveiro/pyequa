
"""
mermaid chart para o artigo

flowchart TD
    I[ignorância] -.-> A(a)
    I[ignorância] -.-> B(b)
    I[ignorância] -.-> C(c)
    A ==>|a+b=10| AB(a b)
    B ==>|a+b=10| AB
    C ==>|a+b=10; 2a+b+c=0| ABC[a b c]
    AB ==>|2a+b+c=0| ABC
    AC(a c) ==>|a+b=10; 2a+b+c=0| ABC
    BC(b c) ==>|a+b=10; 2a+b+c=0| ABC

"""

#
# 4 equações (ou relações)
#
scenary_relations = {
    "Eq(2*a + b + c, 0)",
    "Eq(a + b, 10)",
}



#TODO: 
# Ver "TODO" no ficheiro: 
#  C:\Users\pedrocruz\Documents\GitHub\pyequa\examples\cloze_manyfiles\produtor.py
#

# 6 variáveis
variable_attributes = {
    'a': {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
    'b': {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
    'c': {'type': float, 'tol': 0.01, 'givenvarlevel': 1},
}


# com 4 equações, em geral, consegue-se 4 variáveis
# exemplo: sistema de 4 equações a 4 incógnitas



student_feedback = r"""

(Consulte o docente.)

"""


from pyequa import scenario as ws
from pyequa.servicecloze import ClozeService


# Choose where to store this exercise
from os import getcwd, chdir
print(f"Current file:\n{getcwd()}")
chdir(r"examples\\paperexample")
print(f"Current: {getcwd()}")


text_service = ClozeService(
                 student_template="enunciado.md", 
                 student_feedback=student_feedback, 
                 excel_pathname="dados.xlsx",
                 variable_attributes=variable_attributes,
                 author="Pedro Cruz",
                 sequencial=True,
                 output_extension='md',
                 varcount=1)


#world = ws.Scenario(scenary_relations, text_service,r=[2])
world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]


#plot
#world.draw_wisdom_graph(figsize=[80,80])


# Individual examples
#world.buildall(no_of_given_vars=1, max_ex_per_comb=10) 


# Increased difficult no_of_given_vars=None
#world.buildall(no_of_given_vars=None, max_ex_per_comb=3) 



