import yaml
from os import getcwd, chdir
from pathlib import Path
from pyequa import scenario as ws
from pyequa.servicecloze import ClozeService
import pandas as pd


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
                                     encoding='utf-8')

                case 'xlsx':
                    self.pandas_data_frame = pd.read_excel('data.xlsx')


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


    def exploratory(self):
        self.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 0, 
                                     number_of_problems_per_givenvars = 1)



    def challenge_deterministic(self, 
                                max_combinations_givenvars_per_easynesslevel = 2, 
                                number_of_problems_per_givenvars = 4):

        # Learning from the same exercises for everybody
        
        total_vars = len(self.scenario.allvars_list)

        self.text_service.deterministic_problem_number = 1
        self.text_service.pandas_dataframe_iloc = -1


        # Each new exercises have an increased 'number_of_given_vars': from total_vars-1 to 0.
        for nvars in range(total_vars-1, 0, -1):

            print("="*20)
            print(f"Add exercises with {nvars} given variables.")

            Y = self.scenario.yield_givenvarsset_nodepathlist_from_number(number_of_given_vars=nvars)

            #Control
            count = max_combinations_givenvars_per_easynesslevel

            for problem_pair in Y:

                print(f"==> exercies given {problem_pair[0]}")

                givenvars_set  = problem_pair[0]
                node_path_list = problem_pair[1]

                #General steps for the solution
                self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_set, node_path_list)

                #Abstract method
                self.text_service.challenge_deterministic_add(givenvars_set, node_path_list, number_of_problems_per_givenvars)

                #Decrease counting
                if max_combinations_givenvars_per_easynesslevel: #if there is control
                    count = count - 1 
                    if not count: #when zero
                        break #get out of cycle

        self.conclude()


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

                givenvars_set  = problem_pair[0]
                node_path_list = problem_pair[1]

                #General steps for the solution
                self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_set,node_path_list)

                #Abstract method
                self.text_service.challenge_with_randomquestions_add(var_no, givenvars_set, node_path_list)

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

            givenvars_set  = problem_pair[0]
            node_path_list = problem_pair[1]

            #General steps for the solution
            self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_set,node_path_list)

            #Abstract method
            self.text_service.exam_with_randomquestions_add(givenvars_set, node_path_list, number_of_problems_per_givenvars)


        self.conclude()



    def conclude(self):

        self.text_service.close_build()

        # output_knowledge_graph
        if self.config['output_knowledge_graph']:
            self.scenario.draw_wisdom_graph()

