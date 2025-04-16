import yaml
from os import getcwd, chdir
from pathlib import Path
from pyequa import scenario as ws
from pyequa.servicecloze import ClozeService
import pandas as pd
#from pandas.api.types import is_numeric_dtype
from pandas import Float64Dtype
from pandas import Int64Dtype

# Path to the default configuration file
DEFAULT_CONFIG_PATH = Path(__file__).parent / "default_config.yaml"

def load_config(config_path=None):
    """
    Load configuration from a YAML file.
    If no custom config path is provided, load the default configuration.
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    # start empty
    config = {}

    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

    except FileNotFoundError:
        print(f"File '{config_path}' does not exist.")
    except PermissionError:
        print(f"No permission to access the file '{config_path}'.")
    except IOError:
        print(f"File '{config_path}' cannot be opened for other reasons.")

    return config

def merge_configs(default, user):
    """
    Merge user configuration with default configuration.
    """
    if user is None:
        return default

    for key, value in user.items():
        if isinstance(value, dict) and key in default:
            default[key] = merge_configs(default[key], value)
        else:
            default[key] = value

    return default

# def get_config(user_config_path=None):
#     """
#     Get the final configuration by merging default and user configurations.
#     """
#     default_config = load_config()

#     if user_config_path:
#         user_config = load_config(user_config_path)
#         return merge_configs(default_config, user_config)
#     return default_config

def separate_by_type(input_dict):
    
    """
        # Multichoice com distratores
        'disty':       {'type': 'multichoice',            'givenvarlevel': 2, 
                        'distractors': {'disty_d1': '-33.333', 'disty_d2': '-33.333', 'disty_d3': '-33.333'}},
        # Distratora pura (não é variável de interesse ao problema)
        'nembalagens': {'type': 'distractor'},
    """

    distractors = {}
    non_distractors = {}
    
    for key, var_dict in input_dict.items():

        if var_dict.get('type') == 'distractors' or var_dict.get('type') == 'distractor':
            
            distractors[key] = None
            
        elif 'distractors' in var_dict:

            distractors[key] = var_dict['distractors']
            del var_dict['distractors']
            non_distractors[key] = var_dict

        elif 'distractor' in var_dict:

            distractors[key] = var_dict['distractor']
            del var_dict['distractor']
            non_distractors[key] = var_dict

        elif var_dict.get('type') == 'multichoice':
            
            non_distractors[key] = var_dict

        elif var_dict.get('type') == 'numerical':

            non_distractors[key] = var_dict

        else:

            raise Exception("variable type must be 'distractor' or 'distractors', 'multichoice' or 'numerical'.")    
        
    return distractors, non_distractors



class PyEqua:

    def __init__(self, 
                 exercise_folder=None,
                 scenario_relations=None, 
                 variable_attributes=None, 
                 pandas_data_frame=None):
        """
        - scenario_relations
        - variable_attributes - includes distractors
        - pandas_data_frame
        """
        
        # Load 
        # Load the default configuration
        default_config = load_config()

        chdir(exercise_folder)
        print(f"Exercise folder: {getcwd()}\n\n")
        user_config_path = Path("config.yaml")

        print(f"Reading configuration from {user_config_path}.")
        user_config = load_config(user_config_path)
        config      = merge_configs(default_config, user_config)

        # A config dict is expected to be working now:
        self.config = config
        if 'debug' not in config:
            self.config['debug'] = False


        assert scenario_relations
        self.scenario_relations = scenario_relations

        # separate
        assert variable_attributes
        distractors, non_distractors = separate_by_type(variable_attributes)
        self.variable_attributes = non_distractors
        self.distractors = distractors

        # data_frame creation or use
        if pandas_data_frame is None:

            dataframe_type = self.config['dataframe_type']

            
            match dataframe_type:

                case 'csv':
                    csv_separator = self.config['csv_separator']
                    csv_decimal   = self.config['csv_decimal']

                    self.pandas_data_frame = pd.read_csv('data.csv', 
                                     sep=csv_separator, 
                                     decimal=csv_decimal,
                                     header=0,
                                     index_col=None,
                                     converters = self.mk_converters(),
                                     encoding='utf-8')

                case 'xlsx':
                    self.pandas_data_frame = pd.read_excel('data.xlsx')

        '''
        # Convert, if necessary, dtypes
        # Example: df['col2'] = df['col2'].astype(str)
        for v_name in self.variable_attributes.keys():

            v_type = self.variable_attributes[v_name]["type"]

            if v_type == "numerical":

                #todo
                #if self.pandas_data_frame[v_name].dtype == 
                pass
            
            elif v_type == "multichoice":

                if is_numeric_dtype(self.pandas_data_frame[v_name]):

                    self.pandas_data_frame[v_name].dtype 

                else:

                    self.pandas_data_frame[v_name]
                    



            elif v_type == "distractor": 

                pass

            else:

                raise 
            
            and self.pandas_data_frame[v].dtype 

            '''


        if self.config['output_service'] == 'moodle_cloze':

                self.text_service = ClozeService(
                                student_template_filename = self.config['student_template_filename'], #like "exercise_model.md", 
                                student_feedback = self.config['student_feedback'],
                                answer_template  = self.config['answer_template'],
                                pandas_dataframe    = self.pandas_data_frame,
                                variable_attributes = self.variable_attributes,
                                distractors         = self.distractors,
                                author           = self.config['author'],
                                output_extension = self.config['output_extension'],
                                config           = self.config,
                )

                self.scenario = ws.Scenario(self.scenario_relations, self.text_service) 

        else:

            #TODO: other methods of exporting
            raise ValueError("set config['output_service'] to 'moodle_cloze'")



    def mk_converters(self):
        """
        converters={'col2': str}
        """
        dict_of_converters_1 = {
            var_name: str for var_name in self.variable_attributes.keys() 
               if self.variable_attributes[var_name]['type'] == 'multichoice'
        }
        dict_of_converters_2 = {
            var_name: self.variable_attributes[var_name]['converter'] for var_name in self.variable_attributes.keys() 
               if 'converter' in self.variable_attributes[var_name]
        }

        merged_dict = {**dict_of_converters_1, **dict_of_converters_2}

        return merged_dict
    

    def easy_first(self, 
                   max_number_of_problems=None, 
                   max_combinations_givenvars_per_easynesslevel=None, 
                   number_of_problems_per_givenvars=1):
        # Learning from the same exercises for everybody
        # Easy ones first.

        self.challenge_deterministic(
                   max_number_of_problems, 
                   max_combinations_givenvars_per_easynesslevel, 
                   number_of_problems_per_givenvars,
                   hard_first = False)


    def hard_first(self, 
                   max_number_of_problems=None, 
                   max_combinations_givenvars_per_easynesslevel=None, 
                   number_of_problems_per_givenvars=1):
        # Learning from the same exercises for everybody
        # hard ones first.

        self.challenge_deterministic(
                   max_number_of_problems, 
                   max_combinations_givenvars_per_easynesslevel, 
                   number_of_problems_per_givenvars,
                   hard_first = True)


    def challenge_deterministic(self, 
                   max_number_of_problems=None, 
                   max_combinations_givenvars_per_easynesslevel=None, 
                   number_of_problems_per_givenvars=1,
                   hard_first = True):
        
        # Learning from the same exercises for everybody
        # Difficult ones first.
        
        total_vars = len(self.scenario.allvars_list)

        self.text_service.deterministic_problem_number = 1
        self.text_service.pandas_dataframe_iloc = -1

        problem_number = 1

        if hard_first:
            nvars_range = range(1, total_vars)
        else:
            nvars_range = range(total_vars-1, 0, -1)

        # Each new exercises have an increased 'number_of_given_vars': from total_vars-1 to 0.
        for nvars in nvars_range:

            print("="*20)
            print(f"Add exercises with {nvars} given variables.")

            if hard_first:
                Y = self.scenario.yield_givenvarsset_nodepathlist_from_number(number_of_given_vars=nvars, reverse=True)
            else:
                Y = self.scenario.yield_givenvarsset_nodepathlist_from_number(number_of_given_vars=nvars, reverse=False)

            #Control
            if max_combinations_givenvars_per_easynesslevel: #if there is control
                count_combinations = max_combinations_givenvars_per_easynesslevel

            for problem_pair in Y:

                print(f"==> Adding {number_of_problems_per_givenvars} exercies given {problem_pair[0]}")

                givenvars_tuple  = problem_pair[0]
                node_path_list = problem_pair[1]

                #General steps for the solution
                self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_tuple, node_path_list)

                #Abstract method
                self.text_service.challenge_deterministic_add(givenvars_tuple, node_path_list, number_of_problems_per_givenvars)

                problem_number = problem_number + 1

                #Decrease counting
                if max_combinations_givenvars_per_easynesslevel: #if there is control
                    count_combinations = count_combinations - 1 
                    if count_combinations == 0: #when zero
                        break #get out of cycle

                #Break inner cycle, if needed
                if max_number_of_problems and problem_number > max_number_of_problems:
                    break

            #Break outer cycle, if needed
            if max_number_of_problems and problem_number > max_number_of_problems:
                break


        self.conclude()


    def exploratory(self):
        self.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 0, 
                                     number_of_problems_per_givenvars = 1)



    def challenge_with_randomquestions(self, max_combinations_givenvars_per_easynesslevel = 0):
        # max_combinations_givenvars_per_easynesslevel = 0 means all it can get

        # Learning from the same exercises for everybody
        
        total_vars = len(self.scenario.allvars_list)
        self.text_service.pandas_dataframe_iloc = -1

        # Each new exercises have an increased 'number_of_given_vars': from total_vars-1 to 0.
        problem_number = 1

        for nvars in range(total_vars-1, 0, -1):

            print("="*20)
            print(f"Add exercises with {nvars} given variables.")

            Y = self.scenario.yield_givenvarsset_nodepathlist_from_number(number_of_given_vars=nvars)

            #Controls number of variants
            count = max_combinations_givenvars_per_easynesslevel

            self.text_service.add_problem_header(problem_str = f"{problem_number:02d} with {nvars} given vars")

            for (var_no, problem_pair) in enumerate(Y):

                print(f"==> exercies given {problem_pair[0]}")

                givenvars_tuple  = problem_pair[0]
                node_path_list = problem_pair[1]

                #General steps for the solution
                self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_tuple,node_path_list)

                #Abstract method
                self.text_service.challenge_with_randomquestions_add(var_no, givenvars_tuple, node_path_list)

                #Decrease counting
                if max_combinations_givenvars_per_easynesslevel: #if there is control
                    count = count - 1 
                    if not count: #when zero
                        break #get out of cycle


            problem_number = problem_number + 1


        self.conclude()



    def exam_with_randomquestions(self, fill_in_blanks_vars, number_of_problems_per_givenvars = 1):
        # fill_in_blanks_vars is a set of names

        print("="*20)
        print(f"Generate exercises for fill in the blanks: {fill_in_blanks_vars}.")

        # get symbols from symbol names:
        fill_in_blanks_vars_symbols = [s for s in self.scenario.allvars_set if s.name in fill_in_blanks_vars]

        givenvars_set = self.scenario.allvars_set - set(fill_in_blanks_vars_symbols)

        Y = self.scenario.yield_givenvarsset_nodepathlist_from_varset(givenvars_set)

        self.text_service.pandas_dataframe_iloc = -1

        for problem_pair in Y:

            print(f"==> exercies given {problem_pair[0]}")

            givenvars_tuple  = problem_pair[0]
            node_path_list = problem_pair[1]

            #General steps for the solution
            self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_tuple,node_path_list)

            #Abstract method
            self.text_service.exam_with_randomquestions_add(givenvars_tuple, node_path_list, number_of_problems_per_givenvars)


        self.conclude()



    def conclude(self):

        self.text_service.close_build()

        # output_knowledge_graph
        if self.config['output_knowledge_graph']:
            self.scenario.draw_wisdom_graph()

