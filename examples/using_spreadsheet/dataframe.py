

# Choose where to store this exercise
from os import getcwd, chdir
print(f"Current before: {getcwd()}")
chdir(r"examples/dataframe")
print(f"Current after: {getcwd()}")

from pyequa.clozescenario import ClozeScenario

ClozeScenario(filename=r"df_sc_or_s.xlsx")


#TODO:
# * precisão nos NUMERICAL (integer and float)
# * numerical no excel mas converter a string
