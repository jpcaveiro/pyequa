

import pandas as pd
import os
import datetime
from .serviceabstract import AbstractService, rename_old_filename
from .clozeroutines import Cloze


from .wisdomgraph import set2orderedstr
# Ver:
# self.solverslist_text = self.solverslist_buildtext(givenvars_set,node_path_list)
# self.buildone_scenary_text(givenvars_set)

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
                 answer_template=None,
                 pandas_dataframe=None,
                 variable_attributes=None,
                 distractors = None,
                 author="(Author)",
                 gen_method = 'challenge',
                 output_extension='txt', 
                 number_of_variants_per_exercise=1
                 config=None
                 ): 

        # See AbstractService.__init__()
        super().__init__(pandas_dataframe=pandas_dataframe, 
                         variable_attributes=variable_attributes, 
                         distractors=distractors, 
                         answer_template=answer_template, 
                         gen_method=gen_method, 
                         output_extension=output_extension,
                         config=config)

        # Only in ClozeService
        # student_template could be a filename or a string
        from os import getcwd, chdir
        student_template_path = os.path.join(r'..', student_template)
        print(f"pyequa is opening file {student_template_path}.")
        if '.md' in student_template:
            try:
                with open(student_template_path, mode='r', encoding='utf-8') as file:
                    self.student_template = file.read()
            except FileNotFoundError:
                print(f"Error: File '{student_template}' not found.")
                raise FileNotFoundError
        else:
            self.student_template = student_template


        self.student_feedback = student_feedback

        self.number_of_variants_per_exercise = number_of_variants_per_exercise

        # Counters
        self.problem_no = 0
        self.pandas_dataframe_iloc = -1 # each row of excel "excel/pandas"

        # See serviceabstract.py where self.file_path_student is built
        rename_old_filename(self.file_path_student)

        # Create new file Rmd file
        rmd_header = FILE_HEADER.format(title  = self.file_path_student, 
                                        author = author,
                                        date   = datetime.datetime.now().strftime(r"%Y-%m-%d_%H-%M-%S"))

        if gen_method == 'challenge':
            #Only in case of challenge variants concatenating all problems and their  variants
            problem_header = f"""\n\n# Model {self.file_path_student} - CLOZE\n\n"""
        else:
            problem_header = "" #Empty. Problem header will be added later with their variants.

        with open(self.file_path_student, mode="w", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(rmd_header+problem_header)


    def add_problem_with_variants(self, givenvars_set, node_path_list):
        """
        Produces problems like "rmdmoodle":

        ## Variant <excelrow_no>
        ....

        ## Variant <excelrow_no>
        ....


        Input
        =====

        - givenvars_set : what variables the student knows
        - node_path_list: what nodes, in graph, are part of solution

        """


        if self.gen_method != 'challenge':

            problem_header = f"\n# Problem {self.problem_no+1:02d} - CLOZE\n"
            # ----------------
            # Write header on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(problem_header)



        # Add variants
        for var_no in range(self.number_of_variants_per_exercise):

            # "%" is modulo
            #print(f"debuf: self.pandas_dataframe.index.size = {self.pandas_dataframe.index.size}")
            self.pandas_dataframe_iloc = (self.pandas_dataframe_iloc + 1) % self.pandas_dataframe.shape[0]

            # problem and technical keywords
            args_dict = dict()

            # problem keywords
            pandas_row_series = self.pandas_dataframe.iloc[self.pandas_dataframe_iloc]

            # var+input: student see the value if var is in givenvars_set (ako "given variable")
            # var+input: student see (incógnita) if var is NOT in givenvars_set (ako "determine variable")
            # var+output: student see nothing if var is in givenvars_set
            # var+output: student see value if var is NOT in givenvars_set


            cloze = Cloze(self.pandas_dataframe, 
                          pandas_row_series, 
                          args_dict, 
                          self.scenario.allvars_list, 
                          givenvars_set, 
                          self.variable_attributes,
                          self.distractors,
                          self.config)
            
            args_dict = cloze.vars_to_fields()



            args_dict['answer_steps'] = self.solverslist_answer_text

            if self.gen_method == 'challenge':
                # Variants are added linearly and not separated by different types of problems.
                # problem_no starts at 0. Example:
                # problem_no=0 var_no=0 produce ## Variant 1
                # problem_no=0 var_no=1 produce ## Variant 2
                # problem_no=1 var_no=0 produce ## Variant 3
                # problem_no=1 var_no=1 produce ## Variant 4
                # problem_no=2 var_no=0 produce ## Variant 5
                # problem_no=2 var_no=1 produce ## Variant 6
                # etc
                vno = self.problem_no*self.number_of_variants_per_exercise + (var_no+1)  
            else:
                vno = var_no + 1


            args_dict['variation_number'] = \
                f"{(vno):03d} (data row is {(self.pandas_dataframe_iloc + 1):02d})" # nr. linha pandas + 1 = nr. da linha do excel



            # Nós que fazem parte da solução
            args_dict['nodesequence'] = ', '.join(node_path_list) #node_path_list to text

            #debug
            #print(args_dict)
            # https://docs.python.org/3/library/string.html#string.Formatter.vformat
            # "check_unused_args() is assumed to raise an exception if the check fails.""
            #raise an exception if the check fails

            variant_str = f"\n\n## variante {args_dict['variation_number']}\n\n"
            student_str = self.student_template.format(**args_dict)
            feedback_str = f"\n\n### feedback\n\n{self.student_feedback}\n"

            student_text = variant_str + student_str + feedback_str

            # ----------------
            # Write problem or solution on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)

            #Next number
            self.problem_no += 1                
            



