import pandas as pd
import os
import datetime



from .wisdomgraph import set2orderedstr
# Ver:
# self.solverslist_text = self.solverslist_buildtext(inputvars_set,node_path_list)
# self.buildone_scenary_text(inputvars_set)

class TextService:

    def __init__(self, 
                 student_template, 
                 teacher_template, 
                 answer_template, 
                 excel_pathname=None,
                 basename=None,
                 extension="txt",
                 all_ex_in_samefile=True, 
                 varcount=None,
                 cloze_type = False): #varcount as in rmdmoodle

        self.scenario = None #atribuído quando este TextService é passado para o Scenario
        self.student_template = student_template
        self.teacher_template = teacher_template
        self.answer_template = answer_template
        self.excel_pathname = excel_pathname
        self.basename = basename
        self.extension = extension
        self.all_ex_in_samefile = all_ex_in_samefile
        self.varcount = varcount
        self.cloze_type = cloze_type

        # Excel 
        if self.excel_pathname:
            self.dataframe = pd.read_excel(self.excel_pathname)
        else:
            self.dataframe = None

        # rename previous text files with a timestamp
        if self.basename and self.all_ex_in_samefile:

            #Student problems file
            try:
                # Rename the file saving previously
                student_file_path = f"{self.basename}.{self.extension}"
                new_filename = add_timestamp(student_file_path)
                os.rename(student_file_path, new_filename)
                #os.remove(file_path)
                print(f"File '{student_file_path}' if now {new_filename}.")                
            except FileNotFoundError:
                #print(f"Error: File '{file_path}' not found.")
                pass

            #Teacher problems file
            try:
                # Rename the file saving previously
                file_path_solutions = f"{self.basename}_t.{self.extension}"
                new_filename_solutions = add_timestamp(file_path_solutions)
                os.rename(file_path_solutions, new_filename_solutions)
                #os.remove(file_path)
                print(f"File '{file_path_solutions}' if now {new_filename_solutions}.")
            except FileNotFoundError:
                #print(f"Error: File '{file_path_solutions}' not found.")
                pass

            ex_source_path = os.getcwd()

            student_model_header = f"""# Model {ex_source_path}\n\nProduced in {datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")}\n\n"""
            teacher_model_header = f"""# Solution to model {ex_source_path}\n\nProduced in {datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")}\n\n"""

            # Student file
            with open(f"{self.basename}.{self.extension}", "w", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_model_header)

            # Teacher file
            with open(f"{self.basename}_t.{self.extension}", "w", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(teacher_model_header)



    def buildall_exercises(self,no_of_given_vars,silence):
        self.build_in_silence = silence

        #self.scenario is given when Scenary is instantiated
        Y = self.scenario.yield_inputvarsset_nodepathlist(no_of_given_vars)

        self.dataframe_iloc = -1 # each row of excel "excel/pandas"

        for (problem_no, problem_pair) in enumerate(Y):

            inputvars_set  = problem_pair[0]
            node_path_list = problem_pair[1]

            #General steps for the solution
            self.solverslist_answer_text = self.solverslist_build_answer_text(inputvars_set,node_path_list)

            if self.varcount and self.basename and self.all_ex_in_samefile:
                #"rmdmoodle" style with sections and subsections
                self.add_problem_with_variants(problem_no,inputvars_set,node_path_list)
            else:
                #each excel row, if exists, in a problem
                self.add_problem_linearly(problem_no,inputvars_set,node_path_list)



    def add_problem_with_variants(self,problem_no,inputvars_set,node_path_list):
        """
        Produces problems like "rmdmoodle":

        # Problem n

        ## Variant <excelrow_no>
        ....

        ## Variant <excelrow_no>
        ....


        Input
        =====

        - problem_no : problem number as is generated
        - inputvars_set : what variables the student knows
        - node_path_list: what nodes, in graph, are part of solution

        """

        #debug
        #print("="*10)
        #print("add_problem_with_variants(self,problem_no,inputvars_set,node_path_list)")


        # Add # Problem {problem_no}
        if self.cloze_type:
            problem_header = f"# Problem {problem_no+1:02d} - CLOZE\n"
        else:
            problem_header = f"# Problem {problem_no+1:02d}\n"
        with open(f"{self.basename}.{self.extension}", "a", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(problem_header)
        with open(f"{self.basename}_t.{self.extension}", "a", encoding="utf-8") as file_object:
            # Write the text to the file
            file_object.write(problem_header)

        # Add variants
        for var_no in range(self.varcount):

            # "%" is modulo
            self.dataframe_iloc = (self.dataframe_iloc + 1) % self.dataframe.index.size

            # problem and technical keywords
            args_dict = dict()

            # problem keywords
            pandas_series = self.dataframe.iloc[self.dataframe_iloc]
            for v in self.scenario.allvars_list:
                value = pandas_series[str(v)]
                if v in inputvars_set:
                    args_dict[str(v)+'input'] = value #complicated: f"{value:.4f}"
                    args_dict[str(v)+'output'] = "" #no need to show
                else:
                    if self.cloze_type:
                        args_dict[str(v)+'input'] = f"{{:NUMERICAL:={value}:0.01}}"
                    else:
                        args_dict[str(v)+'input'] = "(incógnita)"
                    args_dict[str(v)+'output'] = value

            # technical keywords
            args_dict['answer_steps'] = self.solverslist_answer_text
            args_dict['variation_number'] = \
                f"{(var_no+1):02d} (excel row is {(self.dataframe_iloc + 1):03d})" # nr. linha pandas + 1 = nr. da linha do excel


            # Nós que fazem parte da solução
            args_dict['nodesequence'] = ', '.join(node_path_list) #node_path_list to text

            #debug
            #print(args_dict)
            # https://docs.python.org/3/library/string.html#string.Formatter.vformat
            # "check_unused_args() is assumed to raise an exception if the check fails.""
            student_text = self.student_template.format(**args_dict) #raise an exception if the check fails
            teacher_text = self.teacher_template.format(**args_dict) #raise an exception if the check fails

            with open(f"{self.basename}.{self.extension}", "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)
            with open(f"{self.basename}_t.{self.extension}", "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(teacher_text)
                if not self.build_in_silence:
                    #For user to imediatly see but
                    #check self.text_service.buildone() for more.
                    print(teacher_text)

        # Add "How did you do it?"
        #HOW =  "# Diz-me como foi? - ESSAY\n\n"
        #HOW += "## Variante Única\n\n"
        #HOW += "Indique a dificuldade (fácil, preciso pensar um pouco, exigente, não consegui ainda):\n\n\n"
        #HOW += "Explique, sucintamente e nas linhas em baixo, que equações foram usadas e ideia das instruções (de software ou calculadora) usados.\n\n\n"
        #HOW += "Obrigado (Equipa docente de MNE).\n"
        #with open(f"{self.basename}.{self.extension}", "a", encoding="utf-8") as file_object:
        #    # Write the text to the file
        #    file_object.write(HOW)
                



    def add_problem_linearly(self,problem_no,inputvars_set,node_path_list):
        """
        Produces the text of an exercise to be concatenated to others.

        Input
        =====

        - problem_no : problem number as is generated
        - inputvars_set : what variables the student knows
        - node_path_list: what nodes, in graph, are part of solution

        """

        args_dict = dict()

        if self.dataframe:
            # if there is a dataframe

            # "%" is modulo
            self.dataframe_iloc = (self.dataframe_iloc+1) % self.dataframe.index.size

            pandas_series = self.dataframe.iloc[self.dataframe_iloc]
            for v in self.scenario.allvars_list:
                value = pandas_series[str(v)]
                if v in inputvars_set:
                    args_dict[str(v)+'input'] = value
                    args_dict[str(v)+'output'] = ""
                else:
                    args_dict[str(v)+'input'] = "(incógnita)"
                    args_dict[str(v)+'output'] = value

        else:
            # there is no data.frame so use "words".
            
            # generic "values"
            VALOR_STR = "some value"
            UNKNOWN_STR = "(unknown value)"
            for v in self.scenario.allvars_list:
                value = pandas_series[str(v)]
                if v in inputvars_set:
                    args_dict[str(v)+'input'] = VALOR_STR
                    args_dict[str(v)+'output'] = ""
                else:
                    args_dict[str(v)+'input'] = UNKNOWN_STR
                    args_dict[str(v)+'output'] = VALOR_STR

        args_dict['answer_steps'] = self.solverslist_answer_text
        args_dict['variation_number'] = self.dataframe_iloc + 1 # nr. linha pandas + 1 = nr. da linha do excel


        # Nós que fazem parte da solução
        args_dict['nodesequence'] = ', '.join(node_path_list) #node_path_list to text

        #debug
        #print(args_dict)
        # https://docs.python.org/3/library/string.html#string.Formatter.vformat
        # "check_unused_args() is assumed to raise an exception if the check fails.""
        student_text = self.student_template.format(**args_dict) #raise an exception if the check fails
        teacher_text = self.teacher_template.format(**args_dict) #raise an exception if the check fails


        if self.basename and self.all_ex_in_samefile:
            #--------------
            # "a" = "append" by renaming with timestamp
            #--------------
            with open(f"{self.basename}.{self.extension}", "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)
            with open(f"{self.basename}_t.{self.extension}", "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(teacher_text)
        elif self.basename and not self.all_ex_in_samefile: #not all_ex_in_samefile
            #----------------------------
            # "w" = "write (overwrite)" (delete previous generated file)
            #----------------------------
            # dataframe_iloc is contiguous from 0 to #excelrows - 1.
            with open(f"{self.basename}_{self.dataframe_iloc+1:002d}.{self.extension}", "w", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)
            with open(f"{self.basename}_{self.dataframe_iloc+1:002d}_t.{self.extension}", "w", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(teacher_text)
        else:
            print(teacher_text)






    def solverslist_build_answer_text(self,inputvars_set,node_path_list):

        #see class Scenario above
        #self.answer_template

        answer_text = ""

        given_vars_node = set2orderedstr(inputvars_set)

        if given_vars_node in node_path_list:
            # If given_vars_node is in the solution path then it is not necessary explain
            # the path from ignorance to given_vars_node.
            nodepair_list = zip(node_path_list[len_inputvars_set:-1], node_path_list[(len_inputvars_set+1):])
        else:
            # If given_vars_node is NOT in the solution path then it is NECESSARY to explain
            # the path from ignorance to knowledge.
            nodepair_list = zip(node_path_list[1:-1], node_path_list[2:])


        len_inputvars_set = len(inputvars_set)

        # node_path_list 
        # node_path_list[len_first_nodes:-1] : 
        # node_path_list[(len_first_nodes+1):]
        for nodepair in nodepair_list:

            if not self.build_in_silence:
                #find edge
                print('-'*3)
                print(f'=>from {nodepair[0]}')
                print(f'=>to   {nodepair[1]}')

            edges = [e for e in self.scenario.wisdomgraph.edges(nodepair[0], data="sc", keys=True) if e[1]==nodepair[1]]
            #edges = list(self.wisdomgraph.edges[nodepair[0]][nodepair[1]]) #, keys=True,))
            
            #There shoulbe be only one element in the above list
            edge = edges[0]

            #Fourth element is a SolverCandidate 
            solver_candidate = edge[3]

            localinputvars = self.scenario.wisdomgraph.nodes[nodepair[0]]['vars']
            localoutputvars = self.scenario.wisdomgraph.nodes[nodepair[1]]['vars']
            solvers = solver_candidate.relations_latex()

            answer_text += self.answer_template.format(
                localinputvars = "{}" if localinputvars==set() else  localinputvars,
                localoutputvars = set(localoutputvars)-set(localinputvars),
                solvers = solvers,
            )

        return answer_text


def add_timestamp(filename):
  """
  Adds a timestamp to the filename in format YYYY-MM-DD_HH-MM-SS.

  Args:
      filename: The original filename (without extension).

  Returns:
      The filename with timestamp appended (including extension).
  """
  timestamp = datetime.datetime.now().strftime(r"%Y-%m-%d_%H-%M-%S")
  # Get the filename extension (if any)
  extension = filename.split(".")[-1] if "." in filename else ""
  # Combine filename, timestamp, and extension
  return f"{filename[:-4]}_{timestamp}.{extension}"

# Example usage
#original_filename = "my_file"
#new_filename = add_timestamp(original_filename)
#print(f"Original: {original_filename}")
#print(f"With Timestamp: {new_filename}")
