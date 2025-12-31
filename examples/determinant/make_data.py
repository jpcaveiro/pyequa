

# Mudar o Python para a pasta deste projeto
from os import chdir
from pathlib import Path
this_file_folder = Path(__file__).parent
chdir(this_file_folder)



# Não é fácil arredondar todos os *.5 para cima!
# TODO: estudar isto
from decimal import Decimal, ROUND_HALF_UP
def round_up_half(number, decimals=1):
    return float(Decimal(str(number)).quantize(Decimal(f'1e-{decimals}'), rounding=ROUND_HALF_UP))


# Função: inputs -> inputs união com outputs
# Implementa o problema na direção direta usual
def make(a11,a12,a21,a22):
    d = a11*a22 - a12*a21
    d = round_up_half(d, 3)
    uniquesolution = "has a unique solution" if d!=0 else "has zero or infinite solutions"

    # locals() tem todas as variáveis locais
    return locals()



# Adding a Row to a Pandas DataFrame from a Dictionary
# https://chat.deepseek.com/a/chat/s/b915bd68-18bc-4179-87c7-27059ae2c4a8


import pandas as pd
df = pd.DataFrame(make(4, 4, 4, 4), index=[0])
df.loc[len(df)] = make(4, 4, 2, 2)
df.loc[len(df)] = make(4, 6, 6, 4)
df.loc[len(df)] = make(1, 0, 3, 4)
df.loc[len(df)] = make(1, 3, 2, 6)


print(df)


df.to_excel("data.xlsx")

