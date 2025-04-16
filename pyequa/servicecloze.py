import os
import datetime
import markdown
from .serviceabstract import AbstractService, rename_old_filename
from .clozeroutines import Cloze


from .scenario import set2orderedstr


FILE_HEADER_template = """---
title: "{title}"
author: "{author}"
date: "{date}"
output:
  html_document: default
---
"""


CLOZE_template_randomquestion = """
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

CLOZE_template_deterministic = """
<question type="category">
    <category>
        <text>$course$/top/{moodle_imports_category}/{exam_title}</text>
    </category>
    <info format="html">
        <text></text>
    </info>
    <idnumber></idnumber>
</question>
<question type="cloze">
    <name>
        <text>{problem_title}</text>
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
                 output_extension='txt', 
                 config=None
                 ): 

        # See AbstractService.__init__()
        super().__init__(pandas_dataframe=pandas_dataframe, 
                         variable_attributes=variable_attributes, 
                         distractors=distractors, 
                         answer_template=answer_template, 
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
                print(f"Error: File '{student_template_path}' not found.")
                raise FileNotFoundError
        else:
            self.student_template_path = student_template_path


        self.student_feedback = student_feedback


        # See serviceabstract.py where self.file_path_student is built
        rename_old_filename(self.file_path_student)

        # -------------------------------
        # Rmd file header for user to see
        # -------------------------------
        rmd_header = FILE_HEADER_template.format(title  = self.file_path_student, 
                                        author = author,
                                        date   = datetime.datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S'))
        with open(self.file_path_student, mode="w", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(rmd_header)


        # ----------------------
        # XML moodle file header
        # ----------------------
        xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
        with open(self.file_path_student+'.xml', mode="w", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(xml_header)



    def challenge_deterministic_add(self, givenvars_set, node_path_list, number_of_problems_per_givenvars):

        # Add problems for this `givenvars_set` (there are no variants)
        # Moodle level is always 1 (no hierarchy)

        # self.deterministic_problem_number

        for _ in range(number_of_problems_per_givenvars):

            # "%" is modulo
            #print(f"debuf: self.pandas_dataframe.index.size = {self.pandas_dataframe.index.size}")
            self.pandas_dataframe_iloc = (self.pandas_dataframe_iloc + 1) % self.pandas_dataframe.shape[0]

            # problem and technical keywords
            #args_dict = dict()

            # problem keywords
            pandas_row_series = self.pandas_dataframe.iloc[self.pandas_dataframe_iloc]

            # var+input: student see the value if var is in givenvars_set (ako "given variable")
            # var+input: student see (incógnita) if var is NOT in givenvars_set (ako "determine variable")
            # var+output: student see nothing if var is in givenvars_set
            # var+output: student see value if var is NOT in givenvars_set


            cloze = Cloze(self.pandas_dataframe, 
                          pandas_row_series, 
                          #args_dict, # all vars values to be replaced in student text model
                          self.scenario.allvars_set, 
                          givenvars_set, 
                          self.variable_attributes,
                          self.distractors,
                          self.config)
            
            args_dict = cloze.vars_to_fields()

            args_dict['answer_steps'] = self.solverslist_answer_text


            args_dict['problem_number_str'] = \
                f"{(self.deterministic_problem_number):03d} (data row is {(self.pandas_dataframe_iloc + 1):02d}) ({givenvars_set})" # nr. linha pandas + 1 = nr. da linha do excel


            # Nós que fazem parte da solução
            args_dict['nodesequence'] = ', '.join(node_path_list) #node_path_list to text

            #debug
            #print(args_dict)
            # https://docs.python.org/3/library/string.html#string.Formatter.vformat
            # "check_unused_args() is assumed to raise an exception if the check fails.""
            #raise an exception if the check fails

            problem_header_str = f"\n\n# {self.config['problem_word']} {args_dict['problem_number_str']}\n\n"

            try:
                student_str = self.student_template.format(**args_dict)
            except KeyError as k:
                print(f"Missing column '{k}' in 'data.{self.config['dataframe_type']}'.")
                raise
                
            feedback_str = f"\n\n\n### feedback\n\n{self.student_feedback}\n\n"

            student_text = problem_header_str + student_str + feedback_str


            # ----------------
            # Markdown: write problem or solution on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)

            self.save_moodle_xml(givenvars_set, args_dict, student_str, 'problem_word', 'problem_number_str')

            r"""
            # ------------
            # Moodle xml: write problem or solution on student and solutions file
            # ------------

            # See https://chat.deepseek.com/a/chat/s/0c4ac66a-c452-490f-9d95-91c22abe1da2
            student_str_without_backslash = student_str.replace(r' \ ~ ', ' ~ ')  
            student_str_html = markdown.markdown(student_str_without_backslash)

            moodle_imports_category = self.config['moodle_import_folder']
            exam_title = self.file_path_student
            problem_title = f"{self.config['problem_word']} {args_dict['problem_number_str']}"
            xml_clozequestion = student_str_html
            xml_feedbackglobal = self.student_feedback

            xml_cloze = CLOZE_template_deterministic.format(
                moodle_imports_category = moodle_imports_category,
                exam_title = exam_title,
                problem_title = problem_title,
                xml_clozequestion = xml_clozequestion,
                xml_feedbackglobal = xml_feedbackglobal,
            )

            with open(self.file_path_student+'.xml', "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(xml_cloze)
            """

            #Next poblem number
            self.deterministic_problem_number = self.deterministic_problem_number + 1


    def challenge_with_randomquestions_add(self, var_no, givenvars_set, node_path_list):


        # "%" is modulo
        #print(f"debuf: self.pandas_dataframe.index.size = {self.pandas_dataframe.index.size}")
        self.pandas_dataframe_iloc = (self.pandas_dataframe_iloc + 1) % self.pandas_dataframe.shape[0]

        # problem and technical keywords
        #args_dict = dict()

        # problem keywords
        pandas_row_series = self.pandas_dataframe.iloc[self.pandas_dataframe_iloc]

        # var+input: student see the value if var is in givenvars_set (ako "given variable")
        # var+input: student see (incógnita) if var is NOT in givenvars_set (ako "determine variable")
        # var+output: student see nothing if var is in givenvars_set
        # var+output: student see value if var is NOT in givenvars_set


        cloze = Cloze(self.pandas_dataframe, 
                        pandas_row_series, 
                        #args_dict, # all vars values to be replaced in student text model
                        self.scenario.allvars_list, 
                        givenvars_set, 
                        self.variable_attributes,
                        self.distractors,
                        self.config)
        
        args_dict = cloze.vars_to_fields()

        args_dict['answer_steps'] = self.solverslist_answer_text


        args_dict['variation_number'] = \
            f"{(var_no+1):03d} (data row is {(self.pandas_dataframe_iloc + 1):02d}) {givenvars_set}" # nr. linha pandas + 1 = nr. da linha do excel



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
            print(f"Missing column '{k}' in 'data.{self.config['dataframe_type']}'.")
            raise
            
        feedback_str = f"\n\n\n### feedback\n\n{self.student_feedback}\n\n"

        student_text = variant_str + student_str + feedback_str

        # ----------------
        # Markdown: write problem or solution on student and solutions file
        # ----------------
        with open(self.file_path_student, "a", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(student_text)


        self.save_moodle_xml(givenvars_set, args_dict, student_str, 'variant_word', 'variation_number')




    def exam_with_randomquestions_add(self, givenvars_set, node_path_list, number_of_variants_per_givenvars):

        self.add_problem_header(problem_str = f"problem given {givenvars_set}")

        # Add variants
        for var_no in range(number_of_variants_per_givenvars):

            # "%" is modulo
            #print(f"debuf: self.pandas_dataframe.index.size = {self.pandas_dataframe.index.size}")
            self.pandas_dataframe_iloc = (self.pandas_dataframe_iloc + 1) % self.pandas_dataframe.shape[0]

            # problem and technical keywords
            #args_dict = dict()

            # problem keywords
            pandas_row_series = self.pandas_dataframe.iloc[self.pandas_dataframe_iloc]

            # var+input: student see the value if var is in givenvars_set (ako "given variable")
            # var+input: student see (incógnita) if var is NOT in givenvars_set (ako "determine variable")
            # var+output: student see nothing if var is in givenvars_set
            # var+output: student see value if var is NOT in givenvars_set


            cloze = Cloze(self.pandas_dataframe, 
                          pandas_row_series, 
                          #args_dict, # all vars values to be replaced in student text model
                          self.scenario.allvars_list, 
                          givenvars_set, 
                          self.variable_attributes,
                          self.distractors,
                          self.config)
            
            args_dict = cloze.vars_to_fields()

            args_dict['answer_steps'] = self.solverslist_answer_text


            args_dict['variation_number'] = \
                f"{(var_no+1):03d} (data row is {(self.pandas_dataframe_iloc + 1):02d})" # nr. linha pandas + 1 = nr. da linha do excel



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
                print(f"Missing column '{k}' in 'data.{self.config['dataframe_type']}'.")
                raise
                
            feedback_str = f"\n\n\n### feedback\n\n{self.student_feedback}\n\n"

            student_text = variant_str + student_str + feedback_str

            # ----------------
            # Markdown: write problem or solution on student and solutions file
            # ----------------
            with open(self.file_path_student, "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)

            self.save_moodle_xml(givenvars_set, args_dict, student_str, 'variant_word', 'variation_number')

            r"""
            # ------------
            # Moodle xml: write problem or solution on student and solutions file
            # ------------

            # See https://chat.deepseek.com/a/chat/s/0c4ac66a-c452-490f-9d95-91c22abe1da2
            student_str_without_backslash = student_str.replace(r' \ ~ ', ' ~ ')
            student_str_html = markdown.markdown(student_str_without_backslash)

            moodle_imports_category = self.config['moodle_import_folder']
            exam_title = self.file_path_student
            question_title = str(givenvars_set)
            variant_title = f"{self.config['variant_word']} {args_dict['variation_number']}"
            xml_clozequestion = student_str_html
            xml_feedbackglobal = self.student_feedback

            xml_cloze = CLOZE_template_randomquestion.format(
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
            """



    def save_moodle_xml(self, givenvars_set, args_dict, student_str, variant_problem_str, args_dict_number):
        # ------------
        # Moodle xml: write problem or solution on student and solutions file
        # ------------

        # See https://chat.deepseek.com/a/chat/s/0c4ac66a-c452-490f-9d95-91c22abe1da2
        student_str_for_pandoc = student_str.replace(r'\~', r'~')
        student_str_for_pandoc = student_str_for_pandoc.replace('\\\n', '\\\\\\\n')
        student_str_for_pandoc = student_str_for_pandoc.replace(r'\[', r'\\[')
        student_str_for_pandoc = student_str_for_pandoc.replace(r'\]', r'\\]')
        student_str_for_pandoc = student_str_for_pandoc.replace(r'\(', r'\\(')
        student_str_for_pandoc = student_str_for_pandoc.replace(r'\)', r'\\)')
        
        #student_str_for_pandoc = student_str_for_pandoc.replace(r'\\', '\\\\\\\\')

        #no extensions
        student_str_html = markdown.markdown(student_str_for_pandoc)#, extensions=[KatexExtension()]) #escape=False)
        student_str_html = student_str_html.replace(r'&amp;', r'&')
        student_str_html = student_str_html.replace(r'\\(', r'\(')
        student_str_html = student_str_html.replace(r'\\)', r'\)')

        #https://gemini.google.com/app/d1a1ca0df542b718
        #student_str_html = markdown.markdown(student_str_without_backslash, escape=False)
        #https://www.perplexity.ai/search/python-markdown-library-avoid-GPLyi_xvSFSjal_JCqM01w?0=r
        #student_str_html = markdown.markdown(student_str_without_backslash, extensions=[KatexExtension()])

        moodle_imports_category = self.config['moodle_import_folder']
        exam_title = self.file_path_student
        question_title = str(givenvars_set)
        variant_title = f"{self.config[variant_problem_str]} {args_dict[args_dict_number]}"
        xml_clozequestion = student_str_html
        xml_feedbackglobal = self.student_feedback

        xml_cloze = CLOZE_template_randomquestion.format(
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

            

    def add_problem_header(self, problem_str):

        problem_header = f"\n# Problem {problem_str} - CLOZE\n"
        # ----------------
        # Write header on student and solutions file
        # ----------------
        with open(self.file_path_student, "a", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(problem_header)



    def close_build(self):
        with open(self.file_path_student+'.xml', "a", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write('\n</quiz>\n')
        
