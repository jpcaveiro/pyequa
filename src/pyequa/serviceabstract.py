import pandas as pd
import os
import datetime


from .scenario import set2orderedstr

from pathlib import Path

def get_last_folder(path):
    """

    ```python
    # Examples
    print(get_last_folder('/path/to/your/folder'))   # Output: 'folder'
    print(get_last_folder('/path/to/your/folder/'))  # Output: 'folder'
    print(get_last_folder('/'))  # Output: '/'
    ```

    """

    path = Path(path)
    # Resolve the path to handle any '..' or '.' and normalize slashes
    resolved_path = path.resolve()
    # Get the last non-empty part
    return resolved_path.parts[-1] if resolved_path.parts[-1] else resolved_path.parts[-2]


class AbstractService:

    def __init__(self,
                 exercise_relativefolder=None,
                 exercise_folder=None, 
                 pandas_dataframe=None,
                 variable_attributes=None,
                 distractors = None,
                 answer_template=None,
                 gen_method='fixed',
                 config=None
                ): 


        self.config = config
        self.exercise_relativefolder = exercise_relativefolder

        assert pandas_dataframe is not None, f"A 'python pandas' data frame must be given."
        self.pandas_dataframe = pandas_dataframe

        # TODO: What if variable_attributes is not given?
        self.variable_attributes = variable_attributes

        # TODO: What if distractors is not given?
        self.distractors = distractors

        # TODO: What if answer_template is not given?
        self.answer_template = answer_template

        self.gen_method = gen_method

        # Delayed: only when "self" is created this variables get instances
        self.scenario = None #atribuído quando este TextService é passado para o Scenario
        self.solverslist_answer_text = None #see below

        #OLD TODO: improve this getcwd() to a better strategy
        self.exercise_folder = exercise_folder
        self.basename = get_last_folder(self.exercise_folder)

        #Create "_output_"
        self.output_folder = Path(self.exercise_folder) / Path("_output_")
        #DEFAULT_OUTPUT_FOLDER =  Path(self.exercise_folder) / Path("_output_")
        if not os.path.exists(self.output_folder ):
            os.makedirs(self.output_folder )
            print(F"Folder '{self.output_folder }' created.")

        self.allexercises_fullpath = self.output_folder / Path(f"{self.basename}.md")

        # Old
        # TODO: avoid change dir !
        #Text is stored here.
        #os.chdir(DEFAULT_OUTPUT_FOLDER)



    def solverslist_build_answer_text(self,givenvars_set,node_path_list):

        #see class Scenario above
        #self.answer_template

        answer_text = ""

        given_vars_node = set2orderedstr(givenvars_set)

        if given_vars_node in node_path_list:
            # If given_vars_node is in the solution path then it is not necessary explain
            # the path from ignorance to given_vars_node.
            nodepair_list = zip(node_path_list[len_givenvars_set:-1], node_path_list[(len_givenvars_set+1):])
        else:
            # If given_vars_node is NOT in the solution path then it is NECESSARY to explain
            # the path from ignorance to knowledge.
            nodepair_list = zip(node_path_list[1:-1], node_path_list[2:])


        len_givenvars_set = len(givenvars_set)

        # node_path_list 
        # node_path_list[len_first_nodes:-1] : 
        # node_path_list[(len_first_nodes+1):]
        for nodepair in nodepair_list:

            if self.config['debug']:
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

            localgivenvars = self.scenario.wisdomgraph.nodes[nodepair[0]]['vars']
            localrequestedvars = self.scenario.wisdomgraph.nodes[nodepair[1]]['vars']
            solvers = solver_candidate.relations_latex()

            answer_text += self.answer_template.format(
                localgivenvars = "{}" if localgivenvars==set() else  localgivenvars,
                localrequestedvars = set(localrequestedvars)-set(localgivenvars),
                solvers = solvers,
            )

        return answer_text



'''
OLD by JP
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
'''

def add_timestamp(filename):
    """
    Adds a timestamp to the filename in format YYYY-MM-DD_HH-MM-SS.

    Args:
        filename: The original filename (str or Path).

    Returns:
        The filename with timestamp appended (including extension).
    By "GPT-5.1-Codex-Max • 0.9x"
    """
    timestamp = datetime.datetime.now().strftime(r"%Y-%m-%d_%H-%M-%S")
    p = Path(filename)
    return str(p.with_name(f"{p.stem}_{timestamp}{p.suffix}"))

def rename_old_filename(allexercises_fullpath):

    #TODO: parece existir repetição da construção destes file_path !

    try:
        # Rename the file saving previously
        timed_path = add_timestamp(allexercises_fullpath)
        os.rename(allexercises_fullpath, timed_path, )
        #os.remove(file_path)
        print(f"File '{allexercises_fullpath}' is now {timed_path}.")                
    except FileNotFoundError:
        #print(f"Error: File '{file_path}' not found.")
        pass


# Example usage
#original_filename = "my_file"
#new_filename = add_timestamp(original_filename)
#print(f"Original: {original_filename}")
#print(f"With Timestamp: {new_filename}")
