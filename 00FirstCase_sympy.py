
# %% setup


#import importlib
#my_module = importlib.import_module('my_module')
#importlib.reload(my_module)



# %% Declaração do modelo


# Declaração do enredo (nome da equação = equação-em-si-mesma).
# https://docs.sympy.org/latest/explanation/gotchas.html#double-equals-signs

from sympy import symbols, Eq

a,b,c,d,e,f = symbols('a,b,c,d,e,f')


eq1   = Eq(f, a+b)
pyt1  = Eq(c**2 + d**2, f**2)
pyt2  = Eq(b**2 + e**2, c**2)
pyt3  = Eq(a**2 + e**2, d**2)
sima1 = Eq(c*e, b*d)
sima2 = Eq(a*c, d*e)
sima3 = Eq(a*b, e**2)
simb1 = Eq(c*d, e*f)
simb2 = Eq(d**2, a*f)
simc1 = Eq(c**2, b*f)

#As condições iniciais são dadas depois:
#a20   = Eq(a, 20)
#b10   = Eq(b, 10)
#c10   = Eq(c, 10)
#e10   = Eq(e, 10)

# declaração do dicionário de variáveis (certamente pode ser automatizado)

scenary = { 
       eq1: {a,b,f},  #eq1 é a equação acima definida e que serve de "key" do dicionário.
      pyt1: {c,d,f},
      pyt2: {b,e,c},
      pyt3: {a,e,d},
      sima1:{c,e,b,d},
      sima2:{a,c,d,e},
      sima3:{a,b,e},
      simb1:{c,d,e,f},
      simb2:{d,a,f},
      simc1:{c,b,f},
      #Ver acima:
      #a20: {a},
      #b10: {b},
      #c10: {c},
      #e10: {e},
     }

#scenary.keys()

# %%


# TODO:
# O que fazer com estes textos? HTML?  Rmd?
# E como colocar equações? e Nomes de variáveis?



scenary_tex = r"""
# essay

Considere a figura

<figura>

# question

Sabe-se que:

{{inputvars}}

Determine: 

{{outputvars}}

## answer

{{answer}}

"""




# %%

#Exemplo em que a<b não funciona
#pois é entendido como comparação de expressões.
#from sympy import symbols, Eq
#a,b = symbols('a,b')
#print(a < b)
#print(sorted({a,b})) 


# %% ====

#import  wisdomgraph as ws



# %% ====================================================


#import  wisdomgraph as ws
import importlib
wisdomgraph = importlib.import_module('wisdomgraph')
importlib.reload(wisdomgraph)


world = wisdomgraph.Scenario(scenary,r=[1,2],scenary_tex=scenary_tex)
#old: sc.build_solvercandidates(r=[1,2])
#old: sc.build_wisdomgraph()

#plot
world.draw_wisdom_graph(figsize=[80,80])


# %%

#print(world.wisdomgraph)

#print(world.combine_and_check_path())

# %%

print(world.combine_and_mk_exercises())


# %%

#TODO Porque combinações de equações é/parece melhor que equações sequênciais?
#TODO: Colocar pesos nas arestas como por exemplo o nr. de equações usadas, ou o nr. de variáveis emvolvidas, no fundo, uma medida de complexidade.



[('ignorance', 'b', "[]->['b']\nEq(b, 10))"), 
 ('b', 'bd', "[]->['d']\nEq(d, 10))"), 
 ('bd', 'abdf', "['b', 'd']->['a', 'f']\nEq(d**2, a*f)\nEq(f, a + b))"), 
 ('abdf', 'abdef', "['a', 'b']->['e']\nEq(a*b, e**2))"), 
 ('abdef', 'knowledge', "['b', 'f']->['c']\nEq(c**2, b*f))")
]


