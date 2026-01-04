
from pathlib import Path


from numpy import sqrt
from scipy.stats import f as f_dist

from decimal import Decimal, ROUND_HALF_UP
def round_up_half(number, decimals=1):
    return float(Decimal(str(number)).quantize(Decimal(f'1e-{decimals}'), rounding=ROUND_HALF_UP))
#print(round_up_half(1.25))  # Output: 1.3
#print(round_up_half(1.35))  # Output: 1.4

def make(x1,x2,x3):
    mean = round_up_half( 1/3*(x1+x2+x3), 3)
    variance = round_up_half( (1/2)*( (x1-mean)**2 + (x2-mean)**2 + (x3-mean)**2 ), 3 )
    cv = round_up_half(sqrt(variance)/mean, 3)
    return locals()
print(make(1.0, 2.0, 3.0))


#def make():  # assuming `make` is your function that generates floats between 0.001 & .999 inclusive, with random decimal points upto two places (i.e., from ~543 through around~678) and rounding to three decimals if necessary
#    return {name: float(f"{value:.2f}") for name, value in locals().items()  # use .format or "%.<nf>s", where n is the number of digits after decimal point. For example ".3g". This will round to three decimals
#    if (isinstance(value, float) and abs(round(value * pow(10,2)) != value)}  # check whether it's a valid floating-point num with two or more digits after decimal point. Otherwise keep as is
    

import pandas as pd
df = pd.DataFrame(make(1.0, 2.0, 3.0), index=[0])
df.loc[len(df)] = make(2.0, 2.0, 4.0)
df.loc[len(df)] = make(3.0, 2.0, 5.0)
df.loc[len(df)] = make(4.0, 2.0, 6.0)
df.loc[len(df)] = make(5.0, 2.0, 7.0)   


print(df)


df.to_excel(Path(__file__).parent / "data.xlsx")