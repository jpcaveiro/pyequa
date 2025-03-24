

# Unilateral mean test at right

# Easy to organize with an idea in mind
alpha  <- c(0.01,  0.01, 0.05, 0.05)
valorp <- c(0.001, 0.05, 0.01, 0.30)

zobs   <- sapply(valorp, function(vp) round(qnorm(1-vp, 0, 1), 4) ) #0.001

rejeitarounao <- mapply( 
    function(vp, a) ifelse(vp < a, 'rejeita-se', 'não se rejeita'), 
    valorp,
    alpha
)

menormaior <- mapply( 
    function(vp, a) ifelse(vp < a, 'é maior', 'é menor'), 
    valorp,
    alpha
)

enaoemaior <- mapply( 
    function(vp, a) ifelse(vp < a, 'é significativamente maior', 'não é significativamente maior'), 
    valorp,
    alpha
)


library(openxlsx)

# Create a sample dataframe
my_dataframe <- data.frame(
  alpha  = alpha,
  valorp = valorp,
  zobs   = zobs,
  rejeitarounao = rejeitarounao,
  menormaior = menormaior,
  enaoemaior = enaoemaior
)

# Save the dataframe to an Excel file
write.xlsx(my_dataframe, file = "dados.xlsx")



