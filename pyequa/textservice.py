import pandas as pd
import os
import datetime

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
                 samefile=True, #keep previous generated files by renaming them
                 varcount=1):

        self.scenario = None #atribuído quando este TextService é passado para o Scenario
        self.student_template = student_template
        self.teacher_template = teacher_template
        self.answer_template = answer_template
        self.excel_pathname = excel_pathname
        self.basename = basename
        self.extension = extension
        self.samefile = samefile
        self.varcount = varcount
        
        # rename previous text files with a timestamp
        if self.basename and self.samefile:
            try:
                # Delete the file
                file_path = f"{self.basename}.{self.extension}"
                new_filename = add_timestamp(file_path)
                os.rename(file_path, new_filename)
                #os.remove(file_path)
                print(f"File '{file_path}' if now {new_filename}.")
            except FileNotFoundError:
                #print(f"Error: File '{file_path}' not found.")
                pass

            try:
                file_path_solutions = f"{self.basename}_t.{self.extension}"
                new_filename_solutions = add_timestamp(file_path_solutions)
                os.rename(file_path_solutions, new_filename_solutions)
                #os.remove(file_path)
                print(f"File '{file_path_solutions}' if now {new_filename_solutions}.")
            except FileNotFoundError:
                #print(f"Error: File '{file_path_solutions}' not found.")
                pass

        if self.excel_pathname:
            self.dataframe = pd.read_excel(self.excel_pathname)
        else:
            self.dataframe = None


    def build_one(self, scenario, inputvars_set, dataframe_iloc, node_path_list):
        """
        Produces the text of an exercise to be concatenated to others.

        Input:

        - inputvars_set
        - outputvars_set
        - solvers_list
        - dataframe_pos
        - node_path_list: indicar ao "teacher" que nós fazem parte da solução

        
        Originalmente foi assim, feito à mão:

            '''
            def author_scenary_text(inputvars_set,outputvars_set,solverslist_text):
                
                #text ver acima

                VALOR = "um valor"
                UNKNOWN = "incónita"

                x1value = VALOR if x1 in inputvars_set else UNKNOWN
                x2value = VALOR if x2 in inputvars_set else UNKNOWN
                x3value = VALOR if x3 in inputvars_set else UNKNOWN

                mediavalue = VALOR if media in inputvars_set else UNKNOWN
                varianciavalue = VALOR if variancia in inputvars_set else UNKNOWN




                print(text.format(
                    x1value = x1value,
                    x2value = x2value,
                    x3value = x3value,
                    mediavalue = mediavalue,
                    varianciavalue = varianciavalue,
                    answer_steps = solverslist_text,
                ))

            '''        
        """



        args_dict = dict()
        if not self.dataframe is None:
            #TODO: programar o varcount!
            #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html#pandas.DataFrame.iloc

            # "%" is modulo
            iloc_modulo = dataframe_iloc % self.dataframe.index.size

            pandas_series = self.dataframe.iloc[iloc_modulo]
            for v in scenario.allvars_list:
                value = pandas_series[str(v)]
                if v in inputvars_set:
                    args_dict[str(v)+'input'] = value
                    args_dict[str(v)+'output'] = ""
                else:
                    args_dict[str(v)+'input'] = "(incógnita)"
                    args_dict[str(v)+'output'] = value
        else:
            VALOR_STR = "um valor"
            UNKNOWN_STR = "incónita"
            for v in scenario.allvars_list:
                args_dict[str(v)+'value'] = VALOR_STR if v in inputvars_set else UNKNOWN_STR

        args_dict['answer_steps'] = scenario.solverslist_answer_text


        # Nós que fazem parte da solução
        args_dict['nodesequence'] = ', '.join(node_path_list) #node_path_list to text

        #debug
        #print(args_dict)
        # https://docs.python.org/3/library/string.html#string.Formatter.vformat
        # "check_unused_args() is assumed to raise an exception if the check fails.""
        student_text = self.student_template.format(**args_dict) #raise an exception if the check fails
        teacher_text = self.teacher_template.format(**args_dict) #raise an exception if the check fails


        if self.basename and self.samefile:
            #--------------
            # "a" = "append" by renaming with timestamp
            #--------------
            with open(f"{self.basename}.{self.extension}", "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)
            with open(f"{self.basename}_t.{self.extension}", "a", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(teacher_text)
        elif self.basename and not self.samefile: #not samefile
            #----------------------------
            # "w" = "write (overwrite)" (delete previous generated file)
            #----------------------------
            with open(f"{self.basename}_{dataframe_iloc+1:02d}.{self.extension}", "w", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(student_text)
            with open(f"{self.basename}_{self.dataframe_iloc+1:02d}_t.{self.extension}", "w", encoding="utf-8") as file_object:
                # Write the text to the file
                file_object.write(teacher_text)
        else:
            print(teacher_text)


        return teacher_text



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

