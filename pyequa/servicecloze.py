

import os
import datetime
import markdown
from .serviceabstract import AbstractService, rename_old_filename
from .clozeroutines import Cloze


from .wisdomgraph import set2orderedstr


FILE_HEADER_template = """---
title: "{title}"
author: "{author}"
date: "{date}"
output:
  html_document: default
---
"""


CLOZE_template = """
<question type="category">
    <category>
        <text>$course$/top/{moodle_imports_category}/{exam_title}/{question_title}</text>
    </category>
    <info format="html">
        <text></text>
    </info>
    <idnumber></idnumber>
</question>
<question type="cloze">
    <name>
        <text>{variant_title} de {question_title}</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[{xml_clozequestion}]]></text>
    </questiontext>
    <generalfeedback format="html">
        <text><![CDATA[{xml_feedbackglobal}]]></text>
    </generalfeedback>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <idnumber></idnumber>
</question>
"""

#
#  xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
#
#  Include sequentialy all CLOZE_template
#  (each CLOZE_template has a path in Moodle Category tree):
#
#     <text>$course$/top/{imports}/{exam_title}/{question_title}</text>
#
#  xml_str = xml_str + '</quiz>\n'
#


class ClozeService(AbstractService):

    def __init__(self, 
                 student_template_filename=None,
                 student_feedback=None,
                 answer_template=None,
                 pandas_dataframe=None,
                 variable_attributes=None,
                 distractors = None,
                 author="(Author)",
                 gen_method = 'challenge',
                 output_extension='txt', 
                 number_of_variants_per_exercise=1,
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
        student_template_path = os.path.join(r'..', student_template_filename)
        print(f"pyequa is opening file {student_template_path}.")
        if '.md' in student_template_filename:
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
        rmd_header = FILE_HEADER_template.format(title  = self.file_path_student, 
                                        author = author,
                                        date   = datetime.datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S'))

        # ----------------------
        # Markdown file: header
        # ----------------------
        if gen_method == 'challenge':

            #Only in case of challenge variants concatenating all problems and their  variants
            rmd_problemheader = f"""\n\n# Model {self.file_path_student} - CLOZE\n\n"""

        else:
            
            rmd_problemheader = "" #Empty. Problem header will be added later with their variants.

        with open(self.file_path_student, mode="w", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(rmd_header+rmd_problemheader)

        # ----------------------
        # Moodle file: header
        # ----------------------
        # Create a new xml file for Moodle
        xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
        with open(self.file_path_student+'.xml', mode="w", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(xml_header)



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

            # ----------------
            # Markdown: Write header on student and solutions file
            # ----------------
            rmd_problemheader = f"\n# Problem {self.problem_no+1:02d} - CLOZE\n"

            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(rmd_problemheader)


            # Moodle xml : see below because Moodle xml repeats
            # the problem header in each varian/problem




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

            variant_str = f"\n\n## {self.config['variant_word']} {args_dict['variation_number']}\n\n"

            try:
                student_str = self.student_template.format(**args_dict)
            except KeyError as k:
                print(f"Missing column '{k}' in 'data.{self.config[self.config['dataframe_type']]}'.")
                raise
                
            feedback_str = f"\n\n### feedback\n\n{self.student_feedback}\n"

            student_text = variant_str + student_str + feedback_str

            # ----------------
            # Markdown: write problem or solution on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)


            # ------------
            # Moodle xml: write problem or solution on student and solutions file
            # ------------

            # See https://chat.deepseek.com/a/chat/s/0c4ac66a-c452-490f-9d95-91c22abe1da2
            student_str_without_backslash = student_str.replace(r'\~', '~')
            student_str_html = markdown.markdown(student_str_without_backslash)

            moodle_imports_category = self.config['moodle_import_folder']
            exam_title = self.config['gen_method']
            question_title = self.file_path_student
            variant_title = f"{self.config['variant_word']} {args_dict['variation_number']}"
            xml_clozequestion = student_str_html
            xml_feedbackglobal = self.student_feedback

            xml_cloze = CLOZE_template.format(
                moodle_imports_category = moodle_imports_category,
                exam_title = exam_title,
                question_title = question_title,
                variant_title = variant_title,
                xml_clozequestion = xml_clozequestion,
                xml_feedbackglobal = xml_feedbackglobal,
            )

            with open(self.file_path_student+'.xml', "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(xml_cloze)

            #Next number
            self.problem_no += 1                
            

    def close_buildall_exercises(self):
        with open(self.file_path_student+'.xml', "a", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write('\n</quiz>\n')
        
