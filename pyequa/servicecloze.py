"""


# Discussion:

# Add "How did you do it?"
#HOW =  "# Diz-me como foi? - ESSAY\n\n"
#HOW += "## Variante Única\n\n"
#HOW += "Indique a dificuldade (fácil, preciso pensar um pouco, exigente, não consegui ainda):\n\n\n"
#HOW += "Explique, sucintamente e nas linhas em baixo, que equações foram usadas e ideia das instruções (de software ou calculadora) usados.\n\n\n"
#HOW += "Obrigado (Equipa docente de MNE).\n"
#with open(f"{self.basename}.{self.extension}", "a", encoding="utf-8") as file_object:
#    # Write the text to the file
#    file_object.write(HOW)
        

"""

import pandas as pd
import os
import datetime
from .serviceabstract import AbstractService, rename_old_filename, DEFAULT_ANSWER_TEMPLATE
from .clozeroutines import Cloze


from .wisdomgraph import set2orderedstr
# Ver:
# self.solverslist_text = self.solverslist_buildtext(inputvars_set,node_path_list)
# self.buildone_scenary_text(inputvars_set)

FILE_HEADER = """---
title: "{title}"
author: "{author}"
date: "{date}"
output:
  html_document: default
---
"""



class ClozeService(AbstractService):

    def __init__(self, 
                 student_template=None, 
                 student_feedback=None, 
                 excel_pathname=None,
                 variable_attributes=None,
                 author="(Author)",
                 answer_template=DEFAULT_ANSWER_TEMPLATE,
                 sequencial = True, 
                 varcount=1): #varcount as in rmdmoodle

        # See AbstractService.__init__()
        super().__init__(excel_pathname,variable_attributes,answer_template)

        # Only in ClozeService
        # student_template could be a filename or a string
        from os import getcwd, chdir
        print(f"Current file 2:\n{getcwd()}")
        if '.md' in student_template:
            try:
                with open(r'..\\'+student_template, mode='r', encoding='utf-8') as file:
                    self.student_template = file.read()
            except FileNotFoundError:
                print(f"Error: File '{student_template}' not found.")
                raise FileNotFoundError
        else:
            self.student_template = student_template


        self.student_feedback = student_feedback
        self.sequencial = sequencial #1 problem with all variants (for study only)
        self.basename, _ = os.path.splitext(os.path.basename(self.excel_pathname))
        if self.sequencial:
            self.basename = self.basename + "-study"
        self.extension = "Rmd"
        self.file_path_student = f"{self.basename}.{self.extension}"
        self.varcount = varcount

        # Counters
        self.problem_no = 0
        self.dataframe_iloc = -1 # each row of excel "excel/pandas"

        rename_old_filename(self.file_path_student)


        # Create new file Rmd file
        rmd_header = FILE_HEADER.format(title = self.file_path_student, 
                                        author = author,
                                        date = datetime.datetime.now().strftime(r"%Y-%m-%d_%H-%M-%S"))

        if self.sequencial:
            #Only in case of sequencial variants concatenating all problems and their  variants
            problem_header = f"""\n\n# Model {self.file_path_student} - CLOZE\n\n"""
        else:
            problem_header = "" #Empty. Problem header will be added later with their variants.

        with open(self.file_path_student, "w", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(rmd_header+problem_header)


    def add_problem_with_variants(self,inputvars_set,node_path_list):
        """
        Produces problems like "rmdmoodle":

        ## Variant <excelrow_no>
        ....

        ## Variant <excelrow_no>
        ....


        Input
        =====

        - inputvars_set : what variables the student knows
        - node_path_list: what nodes, in graph, are part of solution

        """


        if not self.sequencial:

            problem_header = f"\n# Problem {self.problem_no+1:02d} - CLOZE\n"
            # ----------------
            # Write header on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(problem_header)



        # Add variants
        for var_no in range(self.varcount):

            # "%" is modulo
            #print(f"debuf: self.dataframe.index.size = {self.dataframe.index.size}")
            self.dataframe_iloc = (self.dataframe_iloc + 1) % self.dataframe.shape[0]

            # problem and technical keywords
            args_dict = dict()

            # problem keywords
            pandas_series = self.dataframe.iloc[self.dataframe_iloc]

            # var+input: student see the value if var is in inputvars_set (ako "given variable")
            # var+input: student see (incógnita) if var is NOT in inputvars_set (ako "determine variable")
            # var+output: student see nothing if var is in inputvars_set
            # var+output: student see value if var is NOT in inputvars_set


            cloze = Cloze(self.dataframe, pandas_series, args_dict, self.scenario.allvars_list, inputvars_set, self.variable_attributes)
            args_dict = cloze.mk_input_fields()



            args_dict['answer_steps'] = self.solverslist_answer_text

            if self.sequencial:
                # Variants are added linearly and not separated by different types of problems.
                # problem_no starts at 0. Example:
                # problem_no=0 var_no=0 produce ## Variant 1
                # problem_no=0 var_no=1 produce ## Variant 2
                # problem_no=1 var_no=0 produce ## Variant 3
                # problem_no=1 var_no=1 produce ## Variant 4
                # problem_no=2 var_no=0 produce ## Variant 5
                # problem_no=2 var_no=1 produce ## Variant 6
                # etc
                vno = self.problem_no*self.varcount + (var_no+1)  
            else:
                vno = var_no + 1


            args_dict['variation_number'] = \
                f"{(vno):03d} (data row is {(self.dataframe_iloc + 1):02d})" # nr. linha pandas + 1 = nr. da linha do excel



            # Nós que fazem parte da solução
            args_dict['nodesequence'] = ', '.join(node_path_list) #node_path_list to text

            #debug
            #print(args_dict)
            # https://docs.python.org/3/library/string.html#string.Formatter.vformat
            # "check_unused_args() is assumed to raise an exception if the check fails.""
            #raise an exception if the check fails

            variant_str = f"\n\n## variante {args_dict['variation_number']}\n\n"
            student_str = self.student_template.format(**args_dict)
            feedback_str = f"\n### feedback\n\n{self.student_feedback}\n"

            student_text = variant_str + student_str + feedback_str

            # ----------------
            # Write problem or solution on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)

            #Next number
            self.problem_no += 1                
            



