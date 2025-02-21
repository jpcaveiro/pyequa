A probabilidade de acerto no alvo é p={probacerto}.

A variável aleatória

X = "número de acertos no tiro ao alvo em n={n} tiros"

é modelada por uma distribuição Binomial(n,p). 

Então,

P(X menor ou igual a {valorx} | \(X \sim \text{{Binomial}}\)) = {probB}.

O conceito seguinte têm aplicação no Capítulo 3.

Uma Binomial é uma soma de variáveis 0 ou 1 (contagem de sucessos). Então, usando o TLC, uma distribuição Binomial(n,p) aproxima-se a uma distribuição Normal com os seguintes parâmetros: Normal(np, np(1-p)):

* a média da Normal é E[X] = np = {medianormal}
* variância da Normal é Var[X] = np(1-p) = {varnormal}

Usando esta distribuição aproximada,

P(X menor ou igual a {valorx} | \(X \sim_\text{{aprox.}} \text{{Normal}}\)) = {probN}.

Costuma-se usar a seguintes regras que sugerem que a probabilidades calculadas pela Binomial e pela Normal são próximas:

* média da Binomial = \(np \ge 5\) que {verificamedia}, e,
* variância da Binomial = \(np(1-p) \ge 5\) que {verificavar},
* \(n \ge 30 \) que {verifican} (regra usual do TLC),


