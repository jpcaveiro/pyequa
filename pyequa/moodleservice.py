


class Cloze:

    def __init__(self, dataframe, pandas_series, args_dict, allvars_list, inputvars_set):

        # args_dict is to be modified
        self.args_dict = args_dict.copy() # Será copy()?

        # read only
        self.dataframe = dataframe
        self.allvars_list = allvars_list 
        self.inputvars_set = inputvars_set
        self.pandas_series = pandas_series


    def get_unique_answers(self,colname):
        all_possible_answers = self.dataframe[colname].unique()
        return list(all_possible_answers)    
    


    def mk_input_fields(self):



        # ---------------
        # Query dataframe
        # ---------------
        we_know_this = []
        #Debug
        #print(self.inputvars_set)
        for var in self.inputvars_set:
            value = self.pandas_series[var.name]
            #Debug
            #print(type(value))
            #Testar isto:
            if type(value) == str:
                if value[0] == "'":
                    know_this = f"{var} == " + f'''"{value}"'''
                else:
                    know_this = f"{var} == '''{value}'''"
            else:
                know_this = f"{var} == {value}" 
            we_know_this.append(know_this)

            # var+input: student see the value if var is in inputvars_set
            # var+output: student see nothing if var is in inputvars_set

            # var+input: student see {:NUMERICAL/MULTICHOICE: if var is NOT in inputvars_set
            # var+output: student see value if var is NOT in inputvars_set

            self.args_dict[str(var)+'input'] = "**" + str(value) + "**"
            self.args_dict[str(var)+'output'] = ""


        #Debug
        #print(we_know_this)

        # Make query
        query_str = " and ".join(we_know_this)
        #Debug
        #print(query_str)

        #"d" é um dataframe
        d = self.dataframe.query(query_str)
        #Debug
        #print(d)


        #Create cloze inputs for non given variables
        outputvars_set = set(self.allvars_list) - set(self.inputvars_set)
        #Debug
        #print(outputvars_set)



        for var in outputvars_set:

            var_is_stringtype = self.dataframe[var.name].dtype == object

            # saber se é numérico ou str
            #
            # obter unique values
            # saber quais os values corretos: %100%value (os corretos estão na coluna de d)
            # saber quais os values incorretos: %0%value
            # criar a string multichoice

            all_correct_values = d[var.name].unique() #can be just one
            all_unique_values = self.dataframe[var.name].unique()

            more_than_on_correct = len(all_correct_values) > 1

            options_list = []
            for option in all_unique_values:
                if option in all_correct_values:
                    if var_is_stringtype: 
                        options_list.append(f"%100%{option}")
                    else:
                        options_list.append(f"%100%{option}:0.01") #Global tolerance
                else:
                    if var_is_stringtype:
                        options_list.append(f"%0%{option}")
            
            options_str = '\\~'.join(options_list)
            

            if more_than_on_correct:
                more_str = " (indique uma de várias soluções)"
            else:
                more_str = ""

            if var_is_stringtype:
                self.args_dict[var.name+'input'] = "{:MULTICHOICE_S:" + options_str + "}" + more_str
                self.args_dict[var.name+'output'] = options_str
            else:
                self.args_dict[var.name+'input'] = "{:NUMERICAL:" + options_str + "}" + more_str
                self.args_dict[var.name+'output'] = options_str

        #Debug
        #print(self.args_dict)

        return self.args_dict

