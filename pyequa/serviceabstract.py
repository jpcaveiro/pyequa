import pandas as pd
import os
import datetime


from .wisdomgraph import set2orderedstr
# Ver:
# self.solverslist_text = self.solverslist_buildtext(inputvars_set,node_path_list)
# self.buildone_scenary_text(inputvars_set)



DEFAULT_ANSWER_TEMPLATE = """Sabendo

{localinputvars}

e usando

{solvers}

determina-se

{localoutputvars}

"""



class AbstractService:
    """
    
    """

    def __init__(self, 
                 excel_pathname=None,
                 answer_template=DEFAULT_ANSWER_TEMPLATE
                ): 

        self.excel_pathname = excel_pathname
        self.answer_template = answer_template

        #Delayed
        self.scenario = None #atribuído quando este TextService é passado para o Scenario
        self.solverslist_answer_text = None #see below

        #Excel is compulsory
        assert self.excel_pathname, "Excel filename with variables data must be given." + f"({os.getcwd()})"
        self.dataframe = pd.read_excel(self.excel_pathname)


        #Create "_output_"
        DEFAULT_OUTPUT_FOLDER = "_output_"
        if not os.path.exists(DEFAULT_OUTPUT_FOLDER):
            os.makedirs(DEFAULT_OUTPUT_FOLDER)
            print(F"Folder '{DEFAULT_OUTPUT_FOLDER}' created.")

        #Text is stores here.
        os.chdir(DEFAULT_OUTPUT_FOLDER)





    def buildall_exercises(self,no_of_given_vars,max_ex_per_comb,silence):
        self.build_in_silence = silence

        #self.scenario is given when Scenary is instantiated
        Y = self.scenario.yield_inputvarsset_nodepathlist(no_of_given_vars)

        #Controls number of exercises
        count = max_ex_per_comb

        for problem_pair in Y:

            print(f"==> {problem_pair[0]}")

            inputvars_set  = problem_pair[0]
            node_path_list = problem_pair[1]

            #General steps for the solution
            self.solverslist_answer_text = self.solverslist_build_answer_text(inputvars_set,node_path_list)

            #Abstract method
            self.add_problem_with_variants(inputvars_set,node_path_list)

            #Decrease counting
            if max_ex_per_comb: #if there is control
                count = count - 1 
                if not count: #when zero
                    break #get out of cycle










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


def rename_old_filename(file_path_student):

    #TODO: parece existir repetição da construção destes file_path !

    try:
        # Rename the file saving previously
        timed_file_path_student= add_timestamp(file_path_student)
        os.rename(file_path_student,timed_file_path_student, )
        #os.remove(file_path)
        print(f"File '{file_path_student}' is now {timed_file_path_student}.")                
    except FileNotFoundError:
        #print(f"Error: File '{file_path}' not found.")
        pass


# Example usage
#original_filename = "my_file"
#new_filename = add_timestamp(original_filename)
#print(f"Original: {original_filename}")
#print(f"With Timestamp: {new_filename}")
