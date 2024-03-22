
#The Plot

var('a,b,c,d,e,f')



eq1 = f == a+b
pyt1 = c^2 + d^2 == f^2
pyt2 = b^2 + e^2 == c^2
pyt3 = a^2 + e^2 == d^2
sima1 = c*e==b*d
sima2 = a*c==d*e
sima3 = a*b==e^2
simb1 = c*d==e*f
simb2 = d^2==a*f
simc1 = c^2==b*f
b10   = b==10


scenary = { 
       eq1: {a,b,f}, 
      pyt1: {c,d,f},
      pyt2: {b,e,c},
      pyt3: {a,e,d},
      sima1:{c,e,b,d},
      sima2:{a,c,d,e},
      sima3:{a,b,e},
      simb1:{c,d,e,f},
      simb2:{d,a,f},
      simc1:{c,b,f},
      #b10: {b}
     }


import  wisdomgraph as ws
sc = ws.Scenario(scenary)
sc.build_solvercandidates(r=2)
sc.build_wisdomgraph()
print sc.wisdomgraph


