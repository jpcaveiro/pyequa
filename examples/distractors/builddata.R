
# inputs
ndiassemana <- c(3,     4,   5,    6,   7)
valory      <- c(2,     2,   3,    3,   4)
nembalagens <- c(3,    36,  37,   38,  39)
probsucesso <- c(0.5,  0.6, 0.7, 0.8, 0.9)
nsemanas    <- c(10,   20,  30,  40,   50 ) 

# outputs

# corretos
distY <- c("B(3, 0.5)", "B(4, 0.6)", "B(5, 0.7)", "B(6, 0.8)", "B(7, 0.9)")
distY_distrator1 <- c("N(3, 0.5)", "B(4, 0.6)", "B(5, 0.7)", "B(6, 0.8)", "B(7, 0.9)")
distY_distrator2 <- c("Poisson(3)")

# TODO: colocar distratores no setup da variavel quando ela é categória
# Se há distratores, então não usa as outras opções

probvalory <- mapply( 
    function(n,p,v) round( (1 - pbinom(v, n, p)), 3), 
    ndiassemana,
    probsucesso,
    valory
)


# A probabilidade do produto não faltar em nenhum dia ao longo de {nsemamas} é {probsemanas}.
probsemanas <- mapply( 
    function(ns,nds,p) round( (1 - pbinom(0, ns*nds, p)), 3), 
    nsemamas,
    ndiassemana
    probsucesso
)


library(openxlsx)

# Create a sample dataframe
my_dataframe <- data.frame(
  ndiassemana  = ndiassemana,
  valory = valorp,
  nembalagens   = zobs,
  probsucesso = rejeitarounao,
  nsemanas = nsemanas,
  distY = distY,~
  
)

# Save the dataframe to an Excel file
write.xlsx(my_dataframe, file = "dados.xlsx")



