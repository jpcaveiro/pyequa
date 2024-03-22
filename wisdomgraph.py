

"""
# -----------------------------------------------
# wisdomgraph: exercises based on environments 
# 2019 @ Joao Pedro Cruz and Minho Group
# SageMath
# Using python standard libs as much as possible
# -----------------------------------------------
"""

# TODO: dado um wisdomgraph sem enredo, que enredo pode ser criado?


import itertools
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from sympy import Eq

#from sage.all import *


def Combinations(someset):

    from itertools import combinations

    list_of_sets = []

    for i in range(len(someset)+1):
        # Calculate all combinations of size i
        for combo in itertools.combinations(someset, i):
            list_of_sets.append(combo)
            #print(combo)

    return list_of_sets



def set2orderedstr(someset):
    """
    Nota: a < b sendo a e b um sympy.symbol
    causa erro porque não se está a comparar
    o nome mas sim o "conteúdo" do symbol enquanto expressões
    A solução é pedir o str(a).
    """

    return str(sorted([str(s) for s in someset]))


def join_varnames(varlist):

    return "".join( sorted( [str(v) for v in varlist] ) )   


class SolverCandidate:
    """
    A solver candidate is described by:
    
    1. input variables
    2. a list of equation(s)
    3. output variables

    Notation:
    
    - a "solver candidate" has an signature: input variables to outputs variables;
    - it is described also by the equations that can do that
    - at the moment it is not testing if it really solves the equations in order to the output variables
    - "candidate" in the sense that this routine proposes a set of solvers
    - only, later, the "exercise finder" will confirm that it is really possible to solve 

    Input:

    - input_set
    - output_set
    - equations_set

    """


    def __init__(self,input_set,output_set,equations_set):

        #like: 'a+b==2\nc+d==e+g'
        eqstr = '\n'.join( [str(e) for e in equations_set] )

        self.solvername ='{iv}->{ov}\n{eqstr})'.format(
            iv    = set2orderedstr(input_set),
            ov    = set2orderedstr(output_set),
            eqstr = eqstr
        )

        self.signature = {
            'input_set':     input_set, 
            'output_set':    output_set, 
            'equations_set': equations_set
        }


class Scenario:

    _IGNORANCE_NODE_NAME_= 'ignorance'
    _KNOWLEDGE_NODE_NAME_= 'knowledge'


    def __init__(self,scenario,r=[1,2],scenary_tex=""):
        """

        Inputs:

        - scenario: a dictionary like
        - r: list; [1], [2], [1,2], etc

        Combines 1 by 1 equation, and/or 2 by 2, etc.

        .. code:: python

            #variables

            a,b,c,d,e,f = var('a,b,c,d,e,f')

            #The Plot 

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

            # O que fazer com isto?
            b10   = b==10


            scenario = { 
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
            }


        """

        #scenario
        self.scenario = scenario
        self.scenary_tex = scenary_tex

        #special node name (see node_name())
        self.allvars_set = set()
        for eq in scenario.keys():
            self.allvars_set = self.allvars_set.union( scenario[eq] ).copy()

        #TODO: ordenar sympy symbols: não pode ser
        #    direto pois a<b não funciona no sympy
        # Tem que se passar para ['a', 'b', ..] e depois voltar a [a,b,c...]
        #com recurso a dicionário, por exemplo.
        #Ou informar o sympy da str do symbol
        self.allvars_list = list(self.allvars_set)

        #full knowledge: is a node in the wisdom graph
        #that has a name like 'a,b,c,d,e,f' (all vars)
        self.node_knowledge_name = join_varnames(self.allvars_set)
    
        #solver candidates like: (a,b) -> (c,d) using equations
        #populates self.solvercandidates
        self.build_solvercandidates(r)

        #self.wisdomgraph = WisdomGraph()
        self.build_wisdomgraph()




    def mk_solvercandidates(self,eqlist):
        """
        From one equation, or system of equations, produce functions
        based on combinations of variables.

        For example, from `2x + 4y = 10` it produces 2 functions with signatures:

        - x --> y using `2x + 4y = 10` (input variable is `x` and output variable is `y`)
        - y --> x using `2x + 4y = 10` (input variable is `y` and output variable is `x`)

        and likewise with a system of two equations.

        The word "solver" is used because from a set of known variables it produces values for more
        variables. The word "candidate" is used because not always is possible to "solve" the equation(s)
        and produce values for output variables. For example:

        - x --> y using `2x + 4y = 10` (easy to find `y` knowing `x`)
        - y --> x using `x = sqrt(y)` (easy to find `y` but only for a domain in `y`)
        - (2x + y = 4) and (2x + y = 5) has no solution

        See:

        - "Can you give a linear system example of two linear equations and two variables without solution?")
        - https://gemini.google.com/app/cdcb3a9da3f7b97a

        
        A solver candidate is described by:
        
        1. input variables
        2. a list of equation(s)
        3. output variables

        Notation:
        
        - a "solver candidate" has an signature: input variables to outputs variables;
        - it is described also by the equations that can do that
        - at the moment it is not testing if it really solves the equations in order to the output variables
        - "candidate" in the sense that this routine proposes a set of solvers
        - only, later, the "exercise finder" will confirm that it is really possible to solve 
        
        Input:
        
        - eqlist: a list of equations
        
        Output:
        
        - list of solver candidates: [ 
                 {'solvername': solvername,  #an id for graph pourposes
                  'signature': (set of input variables, set of output variables, list of equations) } ]
        
        LINKS:
        
        - https://docs.python.org/3/tutorial/datastructures.html#sets
        
        
        TODO:
        
        - proteger contra duplicados nas equacoes
        
        """
        
        #This function returns a list of solvers
        solver_candidates = []

        #Number of equations
        neq = len(eqlist)

        if neq == 1:
            
            eq = eqlist[0]
            
            #lista de variaveis da unica equacao
            listofvars = list( self.scenario[eq] )

            #All solvers will be formed by: 1 var of output and the rest as input
            for outputvar in listofvars:
                
                #duplica o conjunto (python set -- ver 00FirstCase)
                setofvars =  self.scenario[eq].copy()
                #debug:
                #print("setofvars=",setofvars)
                #print("setofvars type",type(setofvars))

                #remove a var. selecionada para output
                setofvars.remove(outputvar)

                #produz o "solver candidate"
                sc = SolverCandidate(setofvars,{outputvar},{eq})

                solver_candidates.append( sc )
                
            #ver abaixo o return solver_candidates
            
            
        elif neq == 2: #two equations

            #sets of vars from each eq
            listofvarsets = [self.scenario[eq] for eq in eqlist]

            #all vars
            all_vars = set.union( *listofvarsets )

            #TODO: 
            #1. Justificar porque o output só pode ser feito
            #   com a intersecção das vars das equações
            #2. Porque só se considera len(output_vars) == 2 OU len(output_vars) > 2
            #   E se en(output_vars) == 1 ?

            #How many variables in common
            output_vars = set.intersection( *listofvarsets )

            #How many variables in common
            input_vars = all_vars - output_vars

            if len(output_vars) == 2:
                #case: 2 unknowns in 2 equations

                #produz o "solver candidate"
                sc = SolverCandidate(input_vars,output_vars,set(eqlist))

                solver_candidates.append( sc )


            elif len(output_vars) > 2:

                #Caso semelhante ao caso de uma equacao: e' preciso rodar as variaveis.

                #TODO: Este caso deve englobar o caso de cima.

                #selecao de vars que vao ficar 
                #(que vao ser encontradas em sistemas de dois por dois)
                #(as outras vao ser adicionadas aos inputs)

                C = itertools.combinations( output_vars, 2 )
                
                for output_pair in C:

                    set_output_pair = set(output_pair)

                    #Debug
                    #print type(input_vars), type(output_vars), type(set_output_pair)

                    all_inputs = set.union(input_vars, output_vars - set_output_pair)

                    #produz o "solver candidate"
                    sc = SolverCandidate(all_inputs,set_output_pair,set(eqlist))

                    solver_candidates.append( sc )

        else: # neq > 2:
            
            raise NotImplementedError("3 or more equations is not yet implemented.")
        


        #testar uma equacao
        #me_mixed_start([sima2])     
        #testar duas equacoes
        #me_mixed_start([eq1,sima2])    


        return solver_candidates



    def build_solvercandidates(self,r=[1]):
        """
        From scenario, the "self.mk_solvercandidates()" is called 
        to form "solver candidates" from combinations of equations:

        - combinations of all 1 by 1
        - combinations of all 2 by 2
        - else not implemented yet

        
        Input:

        - r: a list ([1],[2], or [1,2]). TODO: complete cases 1, ..., total_number_of_equations

        Output:

        - self.solver_candidates

        """

        self.eqnumber_list = r
        self.solver_candidates = []

        if type(r)==list:

            do_one = 1 in r
            do_two = 2 in r

        else:

            do_one = r==1
            do_two = r==2

        #Note: it can do_one AND do_two
        #      or only one of them.
        if do_one:
            #solver candidates based on 1 equation
            for eq in self.scenario:
                #solver candidates formed from
                #a single equation
                scandidates_1eq = self.mk_solvercandidates([eq])
                self.solver_candidates += scandidates_1eq

        if do_two:
            #solver candidates based on 2 equations
            for eqpair in itertools.combinations(self.scenario, 2):
                #solver candidates formed from
                #two equations
                scandidates_2eq = self.mk_solvercandidates(eqpair)
                self.solver_candidates += scandidates_2eq

        #TODO: considerar mais casos além de "do_one" e "do_two".



    def build_wisdomgraph(self):
        """
        Build a graph from the list of solvers.

        It is called wisdomgraph because nodes, in the wisdom grah, 
        indicate what variables are known until that node.

        References:

        * https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        * https://networkx.org/documentation/stable/reference/classes/generated/networkx.MultiDiGraph.add_edge.html#networkx.MultiDiGraph.add_edge

        Not used:
        * http://doc.sagemath.org/html/en/reference/graphs/sage/graphs/digraph.html
        * https://networkx.org/documentation/stable/reference/classes/digraph.html#networkx.DiGraph

        """

        # populate self.nodes_dict
        self.mk_node_dict()

        self.wisdomgraph = nx.MultiDiGraph()

        #DiGraph().add_nodes_from() 
        #a node is an element from a dict
        self.wisdomgraph.add_nodes_from(self.nodes_dict)

        #para obter o label de um no: "T.get_vertex(1)"

        for s in self.solver_candidates:
            self.add_edge_from_solver(s)




    def node_name(self,varlist):
        """
        Graph nodes must have an easy name (a string).

        Input:

        - varlist

        Output:

        - a string

        Example:

        - a,b,c => abc


        """

        nname = join_varnames(varlist)   

        #nomes especiais

        if nname=='':
            nname = Scenario._IGNORANCE_NODE_NAME_ #'ignorancia'
        elif nname == self.node_knowledge_name:
            nname = Scenario._KNOWLEDGE_NODE_NAME_ #'conhecimento'

        #Debug:
        #print( "node_name=", node_name([f,a]) )

        return nname



    def mk_node_dict(self):
        """
        Each node represents a set of "already known variables".

        A node is a one element dictionary: `{'nodename': set_of_vars}`.

        """

        self.nodes_dict = {} #dictionary: node with labels that are the set of (known) variables

        #Combinations like:
        # C = [ [], [a], [b], .., [a,b], ...,[a,b,c,d,e,f] ]
        C = Combinations( self.allvars_set )

        for varlist in C:  #sagemath is C.list():
            nname = self.node_name(varlist) #makes a str
            self.nodes_dict[nname] = set(varlist)
            #Test
            #print( "{nname} is the set {varlist}.".format(nname=nname,varlist=set(varlist)))

            
    def add_edge_from_solver(self,solver_candidate):
        """
        Each edge represents a "SolverCandidate" that
        receives named variables as input as produces named variables as output
        that represent the "knowledge" acquired by the application
        of the SolverCandidate.
        It is candidate because it could not be feasable: it could produce, due
        to the domain, no solutions.
        """
        
        solver_inputs  = solver_candidate.signature['input_set']
        solver_outputs = solver_candidate.signature['output_set']

        # I is Input
        # O is Output        
        
        for Inode_name in self.nodes_dict.keys():

            #Inode_name is a str

            #set of known variables (a node accessed by str (see node_name()) )

            Ivars = set( self.nodes_dict[Inode_name] )  
            
            if solver_inputs.issubset( Ivars ):

                #output node
                Ovars = Ivars.union(solver_outputs) #.copy() not needed
                
                #make node names
                Inode_name = self.node_name(Ivars)
                Onode_name = self.node_name(Ovars)
                
                if Inode_name!=Onode_name:

                    #If Inode_name == Onode_name then
                    #the solver is not adding new information.
                    #otherwise, add an edge to graph.

                    #add_edge is from nx.DiGraph()
                    self.wisdomgraph.add_edge(Inode_name,Onode_name,key=solver_candidate.solvername)


        #solver1 = {'signature': ({e, c, a}, {d}, a*c == d*e),
        #  'solvername': '[e, c, a]->{d}\na*c == d*e)'}
        #add_edge_from_solver(solver1)  

        #solver_candidates = [solver for solver in me_mixed_start([eq]) for eq in  enredo ]

    def remove_edge_from_solver(self,solver_candidate):
        """
        See remove_edge_from_solver.

        Referência:

        - https://networkx.org/documentation/stable/reference/classes/multidigraph.html

        TODO:

        - explorar a remoção de equações simulando o que se passa se o estudante não se recordar de uma equação.

        """

        edges_to_remove = [ (u,v,key) for (u, v, key) in self.wisdomgraph.edges(keys=True) if key==solver_candidate.solvername]

        self.wisdomgraph.remove_edges_from(edges_to_remove)



    def combine_and_check_path(self):
        """
        From ignorance to single variables: this method

        
        - existence of a path from ignorance to knowledge
        - what is the shortest path from ignorance to knowledge

        Discussion:

        - https://gemini.google.com/app/10274bc0969fab6a

        Naive notes:

        - "sequential" bipartite graph
        - idea: "a set of nodes is a wall if there is no connection" (see graph)
        - there can be edges "jumping walls of nodes"

        Algorithm:

        1. Combine [1 by 1, 2 by 2, ... , n by n] variables
        2. Make edges between "ignorance" and each of those variables.
        3. Count shortest paths between ignorance and knowledge.
        4. Store as txt file.

        
        Example: 
        
        Combining variables into nodes, as before:

        [ (a), (b), .., (ab), (ac), ..., (abc), ..., (abcdef)]

        Note: known at start, for example, (a) and (ef). But this is (aef) and is not enough because
        from (a) one can know other nodes.
           
        [ (a), (b), .., (a,b), (a,c), ..., (abc), ..., (abcdef)]

        New functionality:

        - add and remove edges. 

        Injetar no "scenary" ou só no "wisdom graph"?

        scenary: { Eq(a, 20): {a} }
        wg: self.add_edge_from_solver(SolverCandidate({},{a},{Eq(a,'a')})) 

        """

        C = Combinations(self.allvars_list)

        for somevars in C:

            #Creates edges from ignorance
            #to each var
            for var in somevars:

                #Não funciona porque não adicionar todos os edges
                #Inode_name = Scenario._IGNORANCE_NODE_NAME_
                #Onode_name = self.node_name(set({var}))
                ##add_edge is from nx.DiGraph()
                #self.wisdomgraph.add_edge(Inode_name, Onode_name, name="init.cond.")

                self.add_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set({var}), #output set like {a} (single var)
                        set({Eq(var,10)}) #10 is not used
                    )
                )

            #TODO: configurar 50,50 de forma automatica
            #self.draw_wisdom_graph(figsize=(50,50))

            #Check if has_path
            has_a_path = nx.has_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)

            #Print/Store result
            print("="*10)
            if has_a_path:
                print(f'Há caminho: {somevars}')
            else:
                print(f'Não há caminho: {somevars}')
            print('\n')

            #continue

            #Remove edges 
            for var in somevars:

                self.remove_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set({var}), #output set like {a} (single var)
                        set({Eq(var,10)}) #10 is not used
                    )
                )



        

    def draw_wisdom_graph(self,figsize=[10,10],plot_fn=f'output_{datetime.datetime.now().strftime(r"%y%m%d-%H%M")}.png'):
        """
        based on the number of variables, produce a grid of
        positions for vertices

        sagemath:

        http://doc.sagemath.org/html/en/reference/plotting/sage/graphs/graph_plot.html#sage.graphs.graph_plot.GraphPlot.set_vertices

        ```
        self.wg_plot = self.wisdomgraph.graphplot(
                vertex_size=50,
                talk=True,
                vertex_shape="s",
                vertex_labels=True,
                figsize=figsize)
        return self.wg_plot
        ```

        TODO: será necessário o user 
        fazer isto à mao?

        G.set_pos( {eq1: (1,10), 
                    pyt1: (1,9),
                    pyt2: (1,8),
                    pyt3: (1,7),
                    sima1:(1,6),
                    sima2: (1,5),
                    sima3:(1,4),
                    simb1:(1,3),
                    simb2:(1,2),
                    simc1:(1,1),            
                    a: (5,10),
                    b: (5,9),
                    c: (5,7),
                    d: (5,5),
                    e: (5,2),
                    f: (5,1)
                })

        """

        varlist = self.allvars_list

        nvars = len(varlist)

        comb_length = [ len( list(itertools.combinations(varlist,i)) ) for i in range(nvars+1) ]

        #Debug
        #print comb_length #[1, 6, 15, 20, 15, 6, 1]
        maxcomb = max(comb_length) #20

        
        dx = figsize[0] / (nvars-1)
        dy = figsize[1] / (maxcomb-1)
        
        def sx(i):
            return i*dx

        def sy(j,numcases):
            return (j - numcases//2)*dy

        #maxsize = max( [len(l) for l in comb] )
        #print maxsize

        pos_dic = dict()

        for i in range(nvars+1):

            #Debug
            #print "nvars=",i+1
            
            xpos = sx(i)

            combs = list(itertools.combinations(varlist,i))
            #Debug
            #print "combs=", combs

            for j in range(comb_length[i]):

                ypos = sy(j,comb_length[i])

                #Debug
                #print join_varnames(combs[j]), " fica em (", xpos, ", ", ypos, ")"
                pos_dic[self.node_name(combs[j])] = [xpos,ypos]


        G = self.wisdomgraph

        fig, ax = plt.subplots(figsize=figsize)

        # Draw edge labels using dictionary (optional, uses 'weight' attribute by default)
        #OLDedge_labels_list = [ ((n1,n2),name_str) for n1,n2,name_str in G.edges.data('name')]
        edge_labels_list = [ ((n1,n2),key) for n1,n2,key in G.edges(keys=True)]
        edge_labels_dict = dict(edge_labels_list)
        nx.draw_networkx(G,pos=pos_dic)
        nx.draw_networkx_edge_labels(G, pos=pos_dic, edge_labels=edge_labels_dict)

        plt.savefig(plot_fn)


    def combine_and_mk_exercises(self,maxvars=1):
        """

        Preencher este tipo de strings template:

        ```
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
        ```

        ```python
        mg = nx.MultiGraph()
        mg.add_edge(1, 2, key="k0")
        'k0'
        mg.add_edge(1, 2, key="k1")
        'k1'
        mg.add_edge(2, 3, key="k0")
        'k0'
        for path in sorted(nx.all_simple_edge_paths(mg, 1, 3)):
            print(path)
        [(1, 2, 'k0'), (2, 3, 'k0')]
        [(1, 2, 'k1'), (2, 3, 'k0')]
        ```

        """

        C = Combinations(self.allvars_list)

        gen = (sv for sv in C if len(sv) <= maxvars)

        for somevars in gen:

            #Creates edges from ignorance
            #to each var
            for var in somevars:

                #Não funciona porque não adicionar todos os edges
                #Inode_name = Scenario._IGNORANCE_NODE_NAME_
                #Onode_name = self.node_name(set({var}))
                ##add_edge is from nx.DiGraph()
                #self.wisdomgraph.add_edge(Inode_name, Onode_name, name="init.cond.")

                self.add_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set({var}), #output set like {a} (single var)
                        set({Eq(var,10)}) #10 is not used
                    )
                )

            #TODO: configurar 50,50 de forma automatica
            #self.draw_wisdom_graph(figsize=(50,50))

            #ANTES: Check if has_path
            #has_a_path = nx.has_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)
                
            #AGORA: write all paths (each path is an exercise)
            print("="*10)
            print(f"Caminhos sabendo: {somevars}")
            print("="*10)

            #Shortest
            try:
                node_path_list = list(nx.shortest_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_))

                #for node in node_path_list:
                #    print(node)

                #Os primeiros nós são apenas formados por arestas das
                #condições iniciais:

                l = len(somevars) #len_first_nodes

                print(f"Solution in {len(node_path_list)-l-1} steps.")

                for nodepair in zip(node_path_list[l:-1], node_path_list[(l+1):]):

                    #find edge
                    print('-'*3)
                    print(f'=>from {nodepair[0]}')
                    print(f'=>to   {nodepair[1]}')
                    print('-'*3)
                    edges = list(self.wisdomgraph.edges(nodepair[0], nodepair[1], keys=True))

                    print(edges[0])




            except nx.NetworkXNoPath:
                print("    Não há caminho!")

            
            #ALL paths
            #for path in sorted(nx.all_simple_edge_paths(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)):
            #    print(path)


            #continue

            #Remove edges 
            for var in somevars:

                self.remove_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set({var}), #output set like {a} (single var)
                        set({Eq(var,10)}) #10 is not used
                    )
                )
