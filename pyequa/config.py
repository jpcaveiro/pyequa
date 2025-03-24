import yaml
from pathlib import Path
from pyequa import wisdomgraph as ws
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

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

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



class PyEqua:
    """
    
    Run on user using:

    ```python
    PyEqua().run(scenary_relations,variable_attributes)
    ```

    """

    def __init__(self):
        # Universal File Path Handling in Python

        # Load 
        # Load the default configuration
        config = load_config()

        user_config_path = Path("config.yaml")

        try:

            with open(user_config_path) as _: 
                # File exists and can be opened
                print(f"Reading configuration from {local_config_path}.")
                user_config = load_config(user_config_path)
                config      = merge_configs(config, user_config)

        except FileNotFoundError:
            print("Local 'config.yaml' does not exist.")
        except PermissionError:
            print("No permission to access the file 'config.yaml'.")
        except IOError:
            print("File 'config.yaml' cannot be opened for other reasons.")


        # A config dict is expected to be working now:
        self.config = config


    def run(self, scenary_relations=None, variable_attributes=None, pandas_data_frame=None):
        assert scenary_relations
        assert variable_attributes

        # data_frame creation or use
        if pandas_dataframe is None:

            dataframe_type = self.config['dataframe_type']

            
            match dataframe_type:

                case 'csv':
                    csv_separator = self.config['csv_separator']
                    csv_decimal   = self.config['csv_decimal']

                    pandas_dataframe = pd.read_csv('data.csv', 
                                     sep=csv_separator, 
                                     decimal=csv_decimal,
                                     header=0,
                                     index_col=None,
                                     encoding='utf-8')

                case 'xlsx':
                    pandas_dataframe = pd.read_excel('data.xlsx')


        
        if config['output_service'] == 'moodle_cloze':

                text_service = ClozeService(
                                student_template=config['student_template_filename'] #like "exercise_model.md", 
                                student_feedback=config['student_feedback'],
                                answer_template=config['answer_template'],
                                pandas_dataframe=pandas_dataframe,
                                variable_attributes=variable_attributes,
                                author=config['author'],
                                gen_method=config['gen_method'],
                                output_extension=config['output_extension'],
                                number_of_variants_per_exercise=config['number_of_variants_per_exercise']
                )

                world = ws.Scenario(scenary_relations, text_service) 

                world.buildall(number_of_given_vars=config['number_of_given_vars'], 
                               number_of_variants_per_exercise=config['number_of_variants_per_exercise']) 
        
        else:

            raise ValueError("set config['output_service'] to 'moodle_cloze'")


        # TODO: handle this:
        # output a knowledge graph
        #output_knowledge_graph: false
