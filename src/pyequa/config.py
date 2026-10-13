import yaml
import os #from os import getcwd, chdir
from pathlib import Path
from pyequa import scenario as ws
from pyequa.servicecloze import ClozeService
import pandas as pd
from pandas.api.types import is_numeric_dtype
from .scenario import float2int

#from pandas import Float64Dtype
#from pandas import Int64Dtype


# Old
# Path to the default configuration file
# DEFAULT_CONFIG_PATH = Path(__file__).parent / "default_config.yaml"

PYEQUA_PROJECT_ROOT = os.getenv("PYEQUA_PROJECT_ROOT", "default_if_missing")
if PYEQUA_PROJECT_ROOT == "default_if_missing":
    raise EnvironmentError(
        "Environment variable PYEQUA_PROJECT_ROOT is not set.")
print(f"PYEQUA_PROJECT_ROOT = {PYEQUA_PROJECT_ROOT}")


def separate_by_type(input_dict):
    """
    Split variable metadata into distractors and ordinary answer variables.

    A variable with type ``distractor`` or ``distractors`` is treated as a
    distractor-only column. For answer variables, ``distractor`` or
    ``distractors`` metadata may instead map distractor column names to Moodle
    percentages. Other supported answer types are ``multichoice``,
    ``numerical`` and ``shortanswer``.

    Args:
        input_dict: Mapping from variable names to their metadata dictionaries.
            Entries containing a ``distractor``/``distractors`` mapping are
            updated in place to remove that key.

    Returns:
        A pair ``(distractors, non_distractors)``. The first maps distractor
        answer variables to their options (or ``None`` for distractor-only
        columns); the second maps answer variables to their remaining metadata.

    Raises:
        Exception: If a variable has an unsupported or missing type.
    """

    distractors = {}
    non_distractors = {}
    
    for key, var_dict in input_dict.items():

        if var_dict.get('type') == 'distractors' or var_dict.get('type') == 'distractor':
            
            distractors[key] = None
            
        elif 'distractors' in var_dict:
            #author uses 'distractors'

            distractors[key] = var_dict['distractors']
            del var_dict['distractors']
            non_distractors[key] = var_dict

        elif 'distractor' in var_dict:
            #author uses 'distractor' with no 's'

            distractors[key] = var_dict['distractor']
            del var_dict['distractor']
            non_distractors[key] = var_dict

        elif var_dict.get('type') == 'multichoice':
            
            non_distractors[key] = var_dict

        elif var_dict.get('type') == 'numerical':

            non_distractors[key] = var_dict

        elif var_dict.get('type') == 'shortanswer':

            non_distractors[key] = var_dict

        else:

            raise Exception("variable type must be 'distractor' or 'distractors', 'multichoice', 'numerical' or 'shortanswer'.")    
        
    return distractors, non_distractors


def num2str(value):
    """Format a value as text, removing a zero fractional part when possible.

    For example, ``3.0`` becomes ``"3"`` while ``3.5`` remains ``"3.5"``.
    """
    #if necessary convert to int
    value = float2int(value)
    return f"{value}"




class Config:
    """Load and combine project-wide and exercise-specific YAML settings.

    The project configuration is read from ``config.yaml`` under
    ``PYEQUA_PROJECT_ROOT``. An exercise-level ``config.yaml`` overrides its
    values; if that file cannot be loaded, the project settings are used.
    """

    def __init__(self, exercise_relativefolder):
        """Create the merged configuration for an exercise folder.

        Args:
            exercise_relativefolder: Exercise directory relative to
                ``PYEQUA_PROJECT_ROOT``.
        """
        
        # Load the default configuration
        default_config_path = Path(PYEQUA_PROJECT_ROOT) / Path("config.yaml")
        default_config = self.load_config(default_config_path)

        #old
        #chdir(exercise_folder)
        #print(f"Exercise folder: {getcwd()}\n\n")

        user_config_path = Path(PYEQUA_PROJECT_ROOT) / Path(exercise_relativefolder) / Path("config.yaml")
        print(f"Reading configuration from {user_config_path}.")
        try:
            user_config = self.load_config(user_config_path)
        except:
            user_config = dict()
            print(r"User profile `config.yaml` is not given. Using project configuration.")


        config = self.merge_configs(default_config, user_config)

        if 'debug' not in config:
            config['debug'] = False

        self.config = config


    def load_config(self, config_path=None):
        """Read a YAML configuration file and return its parsed value.

        Args:
            config_path: Path to the YAML file.

        Returns:
            The Python value parsed from the YAML document.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be accessed.
            OSError: If another I/O error occurs while reading it.
        """

        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)

        except FileNotFoundError as ferr:
            print(f"File '{config_path}' does not exist.")
            raise ferr
        except PermissionError as perr:
            print(f"No permission to access the file '{config_path}'.\n\n")
            raise perr
        except IOError as ioerr:
            print(f"File '{config_path}' cannot be opened for other reasons.\n\n")
            raise ioerr

        return config

    def merge_configs(self, default, user):
        """Apply user settings over defaults, recursively for nested mappings.

        Args:
            default: Mutable mapping of default settings; it is updated in
                place.
            user: Mapping of overrides, or ``None`` to leave defaults intact.

        Returns:
            The updated ``default`` mapping.
        """
        if user is None:
            return default

        for key, value in user.items():
            if isinstance(value, dict) and key in default:
                default[key] = self.merge_configs(default[key], value)
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



class PyEqua:
    """Configure and generate equation-based exercises.

    Set ``PYEQUA_PROJECT_ROOT`` and construct an instance with an exercise
    folder, symbolic relations and metadata for each variable. Configuration
    and (unless supplied directly) tabular data are loaded from that folder
    beneath the project root.
    The configured output service currently must be ``moodle_cloze``.

    Exercise generation is started by calling one of the public generation
    methods, such as :meth:`exploratory`, :meth:`easy_first`,
    :meth:`hard_first`, or :meth:`randomquestion_sameblanks`.
    """

    def __init__(self, 
                 exercise_relativefolder=None,
                 scenario_relations=None, 
                 variable_attributes=None, 
                 pandas_data_frame=None):
        """Initialize an exercise from its relations, metadata and data.

        Args:
            exercise_relativefolder: Exercise folder relative to
                ``PYEQUA_PROJECT_ROOT``. Its configuration selects the data
                format and Markdown template.
            scenario_relations: Iterable of SymPy relations or relation
                strings parseable by SymPy.
            variable_attributes: Mapping from variable names to metadata.
                Each answer variable must have a supported ``type``; optional
                fields such as ``tol`` and ``givenvarlevel`` control answer
                checking and exercise ordering. Distractor columns may also be
                declared here.
            pandas_data_frame: Optional pandas DataFrame. If omitted, the
                configured ``data.csv`` or ``data.xlsx`` file is loaded from
                the exercise folder.

        Raises:
            ValueError: If the configured output service is not
                ``moodle_cloze`` or a variable type is unsupported.
        """

        self.exercise_relativefolder = exercise_relativefolder
        self.exercise_folder = Path(PYEQUA_PROJECT_ROOT) / Path(exercise_relativefolder)

        # A config dict (Config(exercise_relativefolder) is an object with config attribute)
        self.config = Config(exercise_relativefolder).config

        assert scenario_relations
        self.scenario_relations = scenario_relations

        # separate
        assert variable_attributes
        distractors, non_distractors = separate_by_type(variable_attributes)
        self.variable_attributes = non_distractors
        self.distractors = distractors

        # data_frame creation or use
        if pandas_data_frame is None:

            # if pandas_data_frame parameter has not been given
            # try to read from data.csv or data.xlsx
            # and this decision in on config.yaml (config object)

            dataframe_type = self.config['dataframe_type']
            
            match dataframe_type:

                case 'csv':
                    csv_separator = self.config['csv_separator']
                    csv_decimal   = self.config['csv_decimal']

                    dataframe_pathname_csv = self.exercise_folder / Path('data.csv')
                    self.pandas_dataframe = pd.read_csv(dataframe_pathname_csv, 
                                     sep=csv_separator, 
                                     decimal=csv_decimal,
                                     header=0,
                                     index_col=None,
                                     converters = self.mk_converters(),
                                     encoding='utf-8')

                case 'xlsx':
                    dataframe_pathname_xlsx = self.exercise_folder / Path('data.xlsx')
                    self.pandas_dataframe = pd.read_excel(dataframe_pathname_xlsx)


        # For each variable, check its
        # self.pandas_dataframe[v_name] dtype
        # and change it if necessary.
        # Example: df['col2'] = df['col2'].astype(str)
        for v_name in self.variable_attributes.keys():

            v_type = self.variable_attributes[v_name]["type"]

            if v_type == "numerical":
                #if is_numeric_dtype(self.pandas_dataframe[v_name])
                #    pass
                #else:
                #    # Try to convert to numerical type
                #    pass 

                pass   
            
            elif v_type == "multichoice":

                if is_numeric_dtype(self.pandas_dataframe[v_name]):

                    # self.pandas_dataframe[v_name].apply(str) não parece funcionar
                    new_values = [num2str(v) for v in self.pandas_dataframe[v_name]]
                    self.pandas_dataframe[v_name] = new_values

            elif v_type == "shortanswer":

                if is_numeric_dtype(self.pandas_dataframe[v_name]):

                    # self.pandas_dataframe[v_name].apply(str) não parece funcionar
                    new_values = [num2str(v) for v in self.pandas_dataframe[v_name]]
                    self.pandas_dataframe[v_name] = new_values

            else:

                raise ValueError(f"pyequa: type of '{var}' is {v_type}: change to 'numerical', 'multichoice' or 'shortanser'.")

            print(f"===> variable {v_name} has pandas type {self.pandas_dataframe[v_name].dtype} and variable_type {self.variable_attributes[v_name]['type']}")

        if self.config['output_service'] == 'moodle_cloze':

                self.text_service = ClozeService(
                                exercise_relativefolder = self.exercise_relativefolder,
                                exercise_folder  = self.exercise_folder,
                                student_template_filename = self.config['student_template_filename'], #like "exercise_model.md", 
                                student_feedback = self.config['student_feedback'],
                                answer_template  = self.config['answer_template'],
                                pandas_dataframe    = self.pandas_dataframe,
                                variable_attributes = self.variable_attributes,
                                distractors         = self.distractors,
                                author           = self.config['author'],
                                config           = self.config,
                )

                self.scenario = ws.Scenario(self, self.scenario_relations, self.text_service) 

        else:

            #TODO: other methods of exporting
            raise ValueError("set config['output_service'] to 'moodle_cloze'")



    def mk_converters(self):
        """Build pandas CSV converters from the variable metadata.

        Multichoice columns are read as strings unless an explicit
        ``converter`` is supplied for that variable.

        Returns:
            A mapping of column names to converter callables.
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
        """Generate deterministic exercises ordered from easier to harder.

        Args:
            max_number_of_problems: Optional cap on the number of generated
                problem sets.
            max_combinations_givenvars_per_easynesslevel: Optional cap on
                given-variable combinations considered at each level.
            number_of_problems_per_givenvars: Number of data-row exercises
                generated for each given-variable combination.
        """
        # Learning from the same exercises for everybody
        # Easy ones first.

        self._challenge_deterministic(
                   max_number_of_problems, 
                   max_combinations_givenvars_per_easynesslevel, 
                   number_of_problems_per_givenvars,
                   hard_first = False)


    def hard_first(self, 
                   max_number_of_problems=None, 
                   max_combinations_givenvars_per_easynesslevel=None, 
                   number_of_problems_per_givenvars=1):
        """Generate deterministic exercises ordered from harder to easier.

        Args:
            max_number_of_problems: Optional cap on the number of generated
                problem sets.
            max_combinations_givenvars_per_easynesslevel: Optional cap on
                given-variable combinations considered at each level.
            number_of_problems_per_givenvars: Number of data-row exercises
                generated for each given-variable combination.
        """
        # Learning from the same exercises for everybody
        # hard ones first.

        self._challenge_deterministic(
                   max_number_of_problems, 
                   max_combinations_givenvars_per_easynesslevel, 
                   number_of_problems_per_givenvars,
                   hard_first = True)


    def _challenge_deterministic(self, 
                   max_number_of_problems=None, 
                   max_combinations_givenvars_per_easynesslevel=None, 
                   number_of_problems_per_givenvars=1,
                   hard_first = True):
        """Generate a deterministic set of exercises in the requested order.

        This internal implementation is shared by :meth:`easy_first`,
        :meth:`hard_first` and :meth:`exploratory`.
        """
        
        # Learning from the same exercises for everybody
        # Difficult ones first.
        
        total_vars = len(self.scenario.allvars_list)

        self.text_service.deterministic_problem_number = 1
        self.text_service.pandas_dataframe_iloc = -1


        if hard_first:
            nvars_range = range(1, total_vars)
        else:
            nvars_range = range(total_vars-1, 0, -1)

        problem_number = 1

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
                self.text_service.challenge_deterministic_add(problem_number,givenvars_tuple, node_path_list, number_of_problems_per_givenvars)
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
        """Generate one deterministic exercise for every reachable givens set.

        Given-variable combinations are ordered from easier to harder and are
        not capped.
        """
        self._challenge_deterministic(
                   max_number_of_problems=None, 
                   max_combinations_givenvars_per_easynesslevel=None, 
                   number_of_problems_per_givenvars=1,
                   hard_first = False)

    def challenge_with_randomquestions(self, max_combinations_givenvars_per_easynesslevel = 0):
        """Generate Moodle questions whose data rows vary across combinations.

        Args:
            max_combinations_givenvars_per_easynesslevel: Maximum number of
                given-variable combinations to include at each level. Zero
                means that all available combinations are included.
        """
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
                self.text_service.challenge_with_randomquestions_add(problem_number, var_no, givenvars_tuple, node_path_list)

                #Decrease counting
                if max_combinations_givenvars_per_easynesslevel: #if there is control
                    count = count - 1 
                    if not count: #when zero
                        break #get out of cycle


            problem_number = problem_number + 1


        self.conclude()



    def randomquestion_sameblanks(self, fill_in_blanks_vars, number_of_problems_per_givenvars = None):
        """Generate fill-in-the-blank exercises for a selected set of variables.

        Args:
            fill_in_blanks_vars: Variable names to leave blank in every
                generated exercise. The other scenario variables are treated
                as given.
            number_of_problems_per_givenvars: Number of data-row variants to
                generate for each reachable solution path. Defaults to the
                number of rows in the underlying DataFrame.
        """

        if number_of_problems_per_givenvars is None:
            number_of_problems_per_givenvars = len(self.pandas_dataframe.index)

        #print("="*20)
        print(f"Generate {number_of_problems_per_givenvars} exercises for fill in the blanks: {fill_in_blanks_vars}.")

        # get symbols from symbol names:
        fill_in_blanks_vars_symbols = [s for s in self.scenario.allvars_set if s.name in fill_in_blanks_vars]

        givenvars_set = self.scenario.allvars_set - set(fill_in_blanks_vars_symbols)

        Y = self.scenario.yield_givenvarsset_nodepathlist_from_varset(givenvars_set)

        self.text_service.pandas_dataframe_iloc = -1

        for (problem_set_number, problem_pair) in enumerate(Y):

            print(f"==> exercies given {problem_pair[0]}")

            givenvars_tuple  = problem_pair[0]
            node_path_list   = problem_pair[1]

            #General steps for the solution
            self.solverslist_answer_text = self.text_service.solverslist_build_answer_text(givenvars_tuple,node_path_list)

            #Abstract method
            self.text_service.randomquestion_sameblanks_add(1, givenvars_tuple, node_path_list, number_of_problems_per_givenvars)


        self.conclude()



    def conclude(self):
        """Finalize generated files and optionally save the scenario graph.

        The Moodle XML quiz is closed by the configured text service. If
        ``output_knowledge_graph`` is enabled, the scenario graph is also
        written to the exercise folder.
        """

        self.text_service.close_build()

        # todo: remove this
        # output_knowledge_graph
        if self.config['output_knowledge_graph']:
            self.scenario.draw_wisdom_graph()
