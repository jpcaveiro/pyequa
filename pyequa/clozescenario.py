"""

# Maneira usando ficheiro "exercicio.py"

text_service = ClozeService(que herda de AbstractService)

scenary_relations = {
    #ws.SR is class Scenary.SympyRelation (ako "equality")
    ws.SR(def_1, latex_str=str(def_1)),
    ws.SR(def_2, latex_str=str(def_2)),
    ws.SR(def_3, latex_str=str(def_3)),
    ws.SR(def_4, latex_str=str(def_4)),
}

world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]

# Maneira usando ficheiro excel

```python
from pyequa.clozescenario import ClozeScenario
world = ClozeScenario(dataframe="excel.xlsx")
#world.draw_wisdom_graph(figsize=[80,80])
all_paths = world.buildall(no_of_given_vars=None, max_ex_per_comb=2)
```

"""

import pandas as pd
import numpy as np
from sympy import Symbol, Eq
from pyequa import wisdomgraph as ws
from pyequa.servicecloze import ClozeService


class ClozeScenario:

    def __init__(self, filename=None, no_of_given_vars=None, max_ex_per_comb=2, author="(author)"):
        
        if '.yaml' in filename:
            raise NotImplemented
        
        #Excel
        self.excel_filename = filename
        all_sheets = pd.read_excel(self.excel_filename, sheet_name=None)  #None = read all sheets
        
        keys_ = list(all_sheets.keys()) #ordered as Excel
        print(all_sheets.keys())

        self.df_data      = all_sheets[keys_[0]] # Data
        self.df_variables = all_sheets[keys_[1]] # Variables
        self.df_relations = all_sheets[keys_[2]] # Relations
        self.df_texts     = all_sheets[keys_[3]] # Texts

        #Adjust dtypes of df_data
        for (i,vtype) in enumerate(list(self.df_variables.iloc[:,1])): #domain column
            if vtype == 'integer':
                if self.df_data.dtypes.iloc[i] == 'int64':
                    pass
                else:
                    #convert
                    raise NotImplemented
            elif vtype == 'string':
                if self.df_data.dtypes.iloc[i] == 'object':
                    pass
                else:
                    #convert
                    raise NotImplemented
            elif vtype == 'float':
                if self.df_data.dtypes.iloc[i] == 'float64':
                    pass
                else:
                    #convert
                    raise NotImplemented

        #Variable create
        for v in list(self.df_variables.iloc[:,0]):
            s = f"{v} = Symbol('{v}')"
            exec(s)

        #Relations create
        scenary_relations = set()
        for l,r in zip( list(self.df_relations.iloc[:,0]),
                        list(self.df_relations.iloc[:,2])
                    ):
            scenary_relations.add( eval( f"ws.SR( Eq({l}, {r}), latex_str='{l}<->{r}' )" ) )


        #Texts
        student_template = self.df_texts.iloc[0,0] #Line 1 in Excel are col names.
        student_feedback = self.df_texts.iloc[2,0]
        answer_template  = self.df_texts.iloc[4,0]

        text_service = ClozeService(
                        student_template=student_template, 
                        student_feedback = student_feedback,
                        answer_template = answer_template,
                        excel_pathname=filename, #get data from sheet 1
                        author=author,
                        sequencial=True,
                        varcount=1)


        #world = ws.Scenario(scenary_relations, text_service,r=[2])
        world = ws.Scenario(scenary_relations, text_service) #implícito que r=[1,2]

        #plot TODO
        #world.draw_wisdom_graph(figsize=[80,80])


        _ = world.buildall(no_of_given_vars=no_of_given_vars, max_ex_per_comb=max_ex_per_comb,silence=True)

