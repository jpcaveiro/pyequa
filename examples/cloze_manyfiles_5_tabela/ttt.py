
from scipy.stats import f as f_dist

def make(sqgrupos, sqerros, dfgrupos, dferros):
    # Calculating Probability from the F-Distribution in Python
    # https://chat.deepseek.com/a/chat/s/f3e50569-f761-4df7-a3c7-b93fbda8cfc2
    sqtotal = sqgrupos + sqerros
    dftotal = dfgrupos + dferros
    msqgrupos = sqgrupos / dfgrupos
    msqerros = sqerros / dferros
    f = msqgrupos/msqerros
    sig = f_dist.sf(f, dfgrupos, dferros)  # Survival function (1 - CDF)
    return locals()
print(make(1,2,3,4))

