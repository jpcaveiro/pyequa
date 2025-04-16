

ALLOWED_PERCENTAGES = {
'100', '90', '80', '75', '70', '66.666', '60', '50', '40', '33.333', '30', '25', '20', '16.666', '14.2857', 
'12.5', '11.111', '10', '5', '0',
'-100', '-90', '-80', '-75', '-70', '-66.666', '-60', '-50', '-40', '-33.333', '-30', '-25', '-20', '-16.666', '-14.2857', 
'-12.5', '-11.111', '-10', '-5', '-0',
}

class Cloze:

    def __init__(self, 
                 pandas_dataframe, 
                 pandas_row_series, 
                 #args_dict, 
                 allvars_set, 
                 givenvars_tuple, 
                 variable_attributes,
                 distractors,
                 config):

        # args_dict is to be modified
        #self.args_dict = args_dict.copy() # copy()?
        self.args_dict = dict()

        # read only
        self.pandas_dataframe = pandas_dataframe
        self.allvars_set = allvars_set 
        self.givenvars_set = set(givenvars_tuple)
        self.pandas_row_series = pandas_row_series
        self.variable_attributes = variable_attributes
        self.distractors = distractors


    def get_distractors_in_columns(self, var):        
        """
        distractors = {
        'disty': {'disty_d1': '-33.333', 'disty_d2': '-33.333', 'disty_d3': '-33.333'},
        'nembalagens': None,
        }
        """

        options_list = None

        if var.name in self.distractors:
            #like 'disty' in distractors

            options_list = []

            for distractor_name in self.distractors[var.name].keys():
                #run over 'disty_d1', 'disty_d2', 'disty_d3'
                option = self.pandas_row_series[distractor_name] #text is series row
                discount = self.distractors[var.name][distractor_name] #from 'disty_d1' we get '-30'
                assert discount in ALLOWED_PERCENTAGES, f"Moodle accepts only {ALLOWED_PERCENTAGES}."
                options_list.append(f"%{discount}%{option}")

        return options_list


    def var_is_stringtype(self, var):  
        #var is an object  

        if self.variable_attributes and var.name in self.variable_attributes:
            # if author gives a dictionary of attributes
            # get type from author specification
            var_is_stringtype = self.variable_attributes[var.name]['type'] in {'multichoice', 'shortanswer'}
        else:
            # if author does NOT gives a dictionary of attributes
            # get type from "excel" / "python dataframe"
            var_is_stringtype = self.pandas_dataframe[var.name].dtype == object

        return var_is_stringtype

    def get_tolerance(self, var):
        if self.variable_attributes and var.name in self.variable_attributes:
            # if author gives a dictionary of attributes
            # get type from author specification
            tol = self.variable_attributes[var.name]['tol']
        else:
            # if author does NOT give a dictionary of attributes
            # get type from "excel" / "python dataframe"
            tol = self.config['global_tolerance']

        return tol


    def vars_to_fields(self):
        """

        This routine builds a args_dict relating:

           variable versus how it appear in a Cloze
        
        Rules:

        1. If a var is in givenvars_set then write it on student exercise text like **10** or **converges**.
        2. If a var is not in givenvars_set (it is a requested var for fill-in-blanks) then write on student 
        exercise like :NUMERICAL: or :MULTICHOICE_S: or :SHORTANSWER:

        Distractors:

        """

        # ---------------
        # A pandas_row_series is selected to make this Cloze.
        # In this row, some are given vars. This given vars have values.
        # The following method is to make a pandas query string to
        # select all rows with same given vars values:  
        #    that query string is called 'we_know_this'
        # ---------------

        #--------------------------------------------
        # Building the vars_dict for given vars.
        # Collecting the aboce explained query.
        #--------------------------------------------

        we_know_this = [] #to make the query of rows_with_same_givenvarsvalues
        #Debug
        #print(self.givenvars_set)
        for var in self.givenvars_set:

            #get variable value in a row (series) of pandas_dataframe
            value = self.pandas_row_series[var.name]

            #Debug
            #print(type(value))

            #Student see the value if var is in givenvars_set:
            if self.variable_attributes[var.name]['type'].lower() == 'multichoice' or \
               self.variable_attributes[var.name]['type'].lower() == 'shortanswer':
                know_this = f"{var} == '''{value}'''"
            else:
                know_this = f"{var} == {value}" 
            we_know_this.append(know_this)

            #The way student sees the variable value
            self.args_dict[var.name] = "**" + str(value) + "**"
            #self.args_dict[str(var)+'output'] = "" #TODO: remove "var+output"



        #Debug
        #print(we_know_this)

        # Make query
        query_str = " and ".join(we_know_this)
        #Debug
        #print(query_str)

        # The following method is to make a pandas query string to
        # select all rows with same given vars values:  
        rows_with_same_givenvarsvalues = self.pandas_dataframe.query(query_str)
        #Debug
        #print(rows_with_same_givenvarsvalues) #it's a pandas dataframe



        #-------------------------------------------------------------
        #Calculating the requested vars (vars to fill-in-the-blanks).
        #(to create cloze inputs for non given variables)
        #-------------------------------------------------------------
        #self.requestedvars_set = set(self.allvars_list) - set(self.givenvars_set)
        self.requestedvars_set = self.allvars_set - self.givenvars_set
        
        #Debug
        #print(self.requestedvars_set)


        #--------------------------------------------
        #Building the vars_dict for requested vars 
        # (vars to fill-in-the-blanks).
        #--------------------------------------------
        for var in self.requestedvars_set: #requested to student as fill-in-the-blanks

            #Both numerical or str variables could have more that
            #one solution considering the given pandas_dataset.
            all_unique_values_for_var  = self.pandas_dataframe[var.name].unique() #several values (one is more rare)
            all_correct_values_for_var = rows_with_same_givenvarsvalues[var.name].unique() #can be just one

            # Debug
            #print(f"len(.) {len(all_correct_values_for_var)}")

            #multichoice, shortanswer, or pandas "object"
            var_is_a_string = self.var_is_stringtype(var)

            # obter unique values
            # saber quais os values corretos: %100%value (os corretos estão na coluna de d)
            # saber quais os values incorretos: %0%value
            # criar a string multichoice

            options_list = []
            
            if var_is_a_string:

                #string type
                for option in all_unique_values_for_var: #all unique values in column "var"
                    if option in all_correct_values_for_var:
                        #In all rows with same givenvarsvalues
                        #there could be several var values and
                        #they are considered correct. Many times
                        #it could be a single value in several rows.
                        options_list.append(f"%100%{option}")

                # Wrong answers can be in distractor variables (columns)
                # or the other values in same var column.
                options_list_wrong_answers = self.get_distractors_in_columns(var)

                if options_list_wrong_answers:
                    #Author provided distrators
                    options_list = options_list + options_list_wrong_answers
                else:
                    #Author did not provided distractors
                    for option in all_unique_values_for_var: #all unique values in column "var"
                        if option not in all_correct_values_for_var:
                            options_list.append(f"%0%{option}")

            else:

                # TODO: dentro do ficheiro Excel
                # há solução única mas na realidade
                # há infinitas soluções: caso do determinante1 Exrc. 8.
                # em que 'det' e 'a11' estão fill-in-the-blanks
                # e, dentro do excel só há uma solução,
                # mas na realidade há infinitas!
                #  
                if len(all_correct_values_for_var)==1:

                    numerical_to_multichoice = False

                    #numerical type: has tolerance
                    tol = self.get_tolerance(var)
                    for option in all_unique_values_for_var:
                        if option in all_correct_values_for_var:
                            options_list.append(f"%100%{option}:{tol}") 

                else:
                    
                    #there are more than one numerical solution:
                    # in this case, convert numerical fill-in-the-bçanks
                    # to multichoice for student could see all values
                    # are to be checked (otherwise only by guessing)

                    numerical_to_multichoice = True

                    #all_unique_values_for_var  = self.pandas_dataframe[var.name].unique() #several values (one is more rare)
                    #all_correct_values_for_var = rows_with_same_givenvarsvalues[var.name].unique() #can be just one



                    for option in all_unique_values_for_var:
                        if option in all_correct_values_for_var:
                            options_list.append(f"%100%{option}") #Not using toleance in multichoice
                    

            
            options_str = '\\~'.join(options_list)
            

            # Determine if: " (more than one solution; choose one) "
            # must appear to student:
            if len(all_correct_values_for_var) > 1:
                more_str = self.config['several_solutions'] # like " (more than one solution; choose one) "
            else:
                more_str = ""


            if self.variable_attributes and \
               var.name in self.variable_attributes and \
               'type' in self.variable_attributes[var.name]:

                #There is variable_attributes:

                match self.variable_attributes[var.name]['type']:
                
                    case 'multichoice':
                        self.args_dict[var.name] = "{:MULTICHOICE_S:" + options_str + "}" + more_str

                    case 'numerical':
                        self.args_dict[var.name] = "{:NUMERICAL:" + options_str + "}" + more_str

                    case 'shortanswer':
                        self.args_dict[var.name] = "{:SHORTANSWER:" + options_str + "}" + more_str
                
                    case _:
                        raise("check variable_attributes for cloze type: 'multichoice', 'numerical' or 'shortanswer'.")
                    
            else:

                # Get from pandas_dataframe type
                if self.pandas_dataframe[var.name].dtype == object:
                    self.args_dict[var.name] = "{:MULTICHOICE_S:" + options_str + "}" + more_str
                else:
                    #assume numerical
                    self.args_dict[var.name] = "{:NUMERICAL:" + options_str + "}" + more_str


        #Add "pure" distractor values of variables
        #By "pure": only polute student undestanding.
        for dis_var_name in self.distractors.keys():

            if self.distractors[dis_var_name] is None: 
                # Empty set means a "pure" distractor.
                # (if no attributes it's a pure distractor)

                #get variable value in a row (series) of pandas_dataframe
                value = self.pandas_row_series[dis_var_name]

                self.args_dict[dis_var_name] = "**" + str(value) + "**"

        #Debug
        #print(self.args_dict)

        return self.args_dict

