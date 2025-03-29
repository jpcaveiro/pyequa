"""
 wisdomgraph: exercises based on environments 
 2019 @ Joao Pedro Cruz and Minho Group
 SageMath
 Using python standard libs as much as possible

 MultiDIGraph from networkx:
 https://networkx.org/documentation/stable/reference/classes/multidigraph.html
"""


import itertools
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from sympy import Eq,Symbol,latex,parse_expr


#from slugify import slugify
#from sage.all import *


def sortedsymbols(symbols_iterable):
    r"""
    Implementação com `key=Symbol._repr_latex_` coloca um \displaystyle
    antes do latex.
    Assim usa-se str()
    """
    return sorted(symbols_iterable,key=Symbol.__str__)


#def symbolslug(s):
#    return slugify(s.__str__())



def Combinations(someset, include_empty_set = True):
    """
    empty = True makes [] part of the answer.
    """

    list_of_sets = []

    if include_empty_set:
        start = 0  #itertools.combinations(someset, 0) produce empty set
    else:
        start = 1

    for i in range(start,len(someset)+1):
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







class SympyRelation:
    """
    A ideia é associar a uma expressão sympy:
    * uma forma latex
    * os símbolos na relação

    >> x1 = Symbol('x_1')
    >> x2 = Symbol('x_2')
    >> x3 = Symbol('x_3')
    >> media = Symbol('\\bar{x}')
    >> SympyRelation( Eq(media, Rational(1,3)*(x1+x2+x3)) )

    """
    
    def __init__(self,sympyrelation,free_symbols=None,latex_str="", input_is_str=False):
        
        if input_is_str:
            self.sympyrelation = parse_expr(sympyrelation)
        else:
            self.sympyrelation = sympyrelation

        if free_symbols:
            self.free_symbols = free_symbols
        else:
            self.free_symbols = self.sympyrelation.free_symbols

        if latex_str:
            self.latex_str = latex_str
        else:
            self.latex_str = latex(self.sympyrelation)

    def __str__(self):
        return self.latex_str
    
    def __repr__(self):
        return f"SympyRelation({self.sympyrelation},{self.free_symbols},{self.latex_str})"

SR = SympyRelation        



class SolverCandidate:
    """
    A solver candidate is described by:
    
    1. input variables
    2. a set of expressions(s)
    3. output variables

    Notation:
    
    - a "solver candidate" has an signature: input variables to outputs variables;
    - it is described also by the relations that can do that
    - at the moment it is not testing if it really solves the relations in order to the output variables
    - "candidate" in the sense that this routine proposes a set of solvers
    - only, later, the "exercise finder" will confirm that it is really possible to solve 

    Input:

    - input_set
    - output_set
    - relations_set

    """


    def __init__(self,input_set,output_set,relations_set):

        #like: 'a+b==2\nc+d==e+g'
        rel_str = '\n'.join( [e.latex_str for e in relations_set] )

        
        self.solvername ='{iv}->{ov}\n{rel_str})'.format(
            iv    = set2orderedstr(input_set),
            ov    = set2orderedstr(output_set),
            rel_str = rel_str
        )

        self.signature = {
            'input_set':     input_set, 
            'output_set':    output_set, 
            'relations_set': relations_set
        }

    def relations_latex(self):
        return '\n\n'.join([r.latex_str for r in self.signature['relations_set']])



class Scenario:

    _IGNORANCE_NODE_NAME_ = 'ignorance'
    _KNOWLEDGE_NODE_NAME_ = 'knowledge'

    def __init__(self, scenario_relations, text_service, list_of_number_of_relations_at_once=None):
        """

        Inputs:

        - scenario: a dictionary like
        - r: list; [1], [2], [1,2], etc

        Combines 1 by 1 relation, and/or 2 by 2, etc.

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


            scenario_equations = { 
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
        #scenario_relations can be: a set of str or a set of SR (see above):

        self.scenario_relations_set = set()
        for eq in scenario_relations:
            if type(eq) == str:
                self.scenario_relations_set.add(SR(eq,latex_str=eq,input_is_str=True)) #str to a "wisdomgraph.SR" objet
            else:
                self.scenario_relations_set.add(eq) #here user provid a wisdomgraph.SR objet

        self.text_service = text_service
        self.text_service.scenario = self
        #self.answer_template = answer_template


        #special node name (see node_name()) #TODO: distractor variables does not appear in relations
        self.allvars_set = set()
        for rel in self.scenario_relations_set:
            self.allvars_set = self.allvars_set.union( rel.free_symbols ).copy()

        #TODO: ordenar sympy symbols: não pode ser
        #    direto pois a<b não funciona no sympy
        # Tem que se passar para ['a', 'b', ..] e depois voltar a [a,b,c...]
        #com recurso a dicionário, por exemplo.
        #Ou informar o sympy da str do symbol
        self.allvars_list = list(self.allvars_set)

        #full knowledge: is a node in the wisdom graph
        #that has a name like 'a,b,c,d,e,f' (all vars)
        self.node_knowledge_name = join_varnames(self.allvars_set)
    


        if not list_of_number_of_relations_at_once:
            list_of_number_of_relations_at_once = list(range(1, len(self.scenario_relations_set) + 1))
        self.list_of_number_of_relations_at_once = list_of_number_of_relations_at_once


        #build all solver candidates like: (a,b) -> (c,d) from relations
        #Populates:
        # self.rel_number_list = a number 1, 2, or more relations at same time
        # self.solver_candidates_list = a list of edges; below a graph with this edges is formed
        self.buildall_solvercandidates()


        #Makes a MuliDiGraph where nodes represent "known vars at the moment"
        #and edges are "operators" that moves from one node to another.
        #Populates: 
        # self.wisdomgraph - nx.MuliDiGraph
        # self.nodes_dict - a dictionary where each key is made by a label formed by a set of variables
        #                   each key points to the respective set of variables; it is understood to be the node
        #                   of the graph; each node means those variables are known at that time.
        self.build_wisdomgraph()


    def input_level(self, var_combination):
        """
        example input:

        - var_combination is {var1,var2,var3}

        example output:

        - 

        
        'probacerto':  {'type': float, 'tol': 0.001, 'givenvarlevel': 1},
        """

        input_level_sum = 0
        for var in var_combination:
            #var is a sympy symbol
            var_str = str(var)
            if self.text_service.variable_attributes and var_str in self.text_service.variable_attributes:
                # if an author has defined attributes for var
                if 'givenvarlevel' in self.text_service.variable_attributes[var_str]:
                    # if 'givenvarlevel' has defined by the autor
                    level = self.text_service.variable_attributes[var_str]['givenvarlevel']
                    input_level_sum += level
                else:
                    input_level_sum += 1
            else:
                input_level_sum += 1

        return input_level_sum      


    def buildsome_solvercandidates(self, rel_set): 
        """
        From one relation, or system of relations, produce functions
        based on combinations of variables.

        For example, from `2x + 4y = 10` it produces 2 functions with signatures:

        - x --> y using `2x + 4y = 10` (input variable is `x` and output variable is `y`)
        - y --> x using `2x + 4y = 10` (input variable is `y` and output variable is `x`)

        and likewise with a system of two relations.

        The word "solver" is used because from a set of known variables it produces values for more
        variables. The word "candidate" is used because not always is possible to "solve" the relations(s)
        and produce values for output variables. For example:

        - x --> y using `2x + 4y = 10` (easy to find `y` knowing `x`)
        - y --> x using `x = sqrt(y)` (easy to find `y` but only for a domain in `y`)
        - (2x + y = 4) and (2x + y = 5) has no solution

        See:

        - "Can you give a linear system example of two linear relations and two variables without solution?")
        - https://gemini.google.com/app/cdcb3a9da3f7b97a

        
        A solver candidate is described by:
        
        1. input variables
        2. a list of relations
        3. output variables

        Notation:
        
        - a "solver candidate" has an signature: input variables to outputs variables;
        - it is described also by the relations that can do that
        - at the moment it is not testing if it really solves the relations in order to the output variables
        - "candidate" in the sense that this routine proposes a set of solvers
        - only, later, the "exercise finder" will confirm that it is really possible to solve 
        
        Input:
        
        - rellist: a list of relations
        
        Output:
        
        - list of solver candidates: [ 
                 {'solvername': solvername,  #an id for graph pourposes
                  'signature': (set of input variables, set of output variables, list of relations) } ]
        
        LINKS:
        
        - https://docs.python.org/3/tutorial/datastructures.html#sets
        
        
        TODO:
        
        - proteger contra duplicados nas relações
        

        """
        

        #This function returns a list of solvers
        solver_candidates = []

        #Number of relations
        nrel= len(rel_set)

        #Something like [ {v1,v2}, {v1,v3}, etc ]
        listofvarsets = [rel.free_symbols for rel in rel_set]

        #All vars in the rel_set
        all_vars_in_rel_set = set.union( *listofvarsets )

        #Variables in common 
        candidate_output_vars_set = set.intersection( *listofvarsets )

        #How many variables should be known in advance
        must_be_known_vars_in_rel_set = all_vars_in_rel_set - candidate_output_vars_set

        #There are `nrel` relations to be used to produce solvers
        combinations_of_output_vars_set = itertools.combinations( candidate_output_vars_set, nrel )

        for output_vars_combination in combinations_of_output_vars_set:

            output_vars_set = set(output_vars_combination)
            
            assert(type(output_vars_set) == set)

            known_vars_set_for_this_case  = set.union(must_be_known_vars_in_rel_set, candidate_output_vars_set - output_vars_set)

            #Produce "solver candidate"
            sc = SolverCandidate(known_vars_set_for_this_case, output_vars_set, set(rel_set))

            solver_candidates.append( sc )

        return solver_candidates




    def buildall_solvercandidates(self):
        """

        Inputs:

        - `self.list_of_number_of_relations_at_once`: is a list

        Output:

        - self.solver_candidates_list

        Idea:

        * To find 1 unknown (1 variable), it is needed 1 equation (or relation) with that variable in commom.
        * To find 2 unknowns (2 variables), it is needed 2 equations (or relations) with those variables in commom.
        * To find 3 unknowns (3 variables), it is needed 3 equations (or relations) with those variables in commom.
        * etc

        Numbers in `list_of_number_of_relations_at_once` define the number of 
        unknowns (or variables) that student must find given something that is already known.

        From scenario, the "self.buildall_solvercandidates()" is called 
        to form "solver candidates" from combinations of relations.

        """

        # The input is part of self:
        # self.list_of_number_of_relations_at_once

        self.solver_candidates_list = []

        for nrel in self.list_of_number_of_relations_at_once:

            #self.relnumber_list = r

            for rel_set in itertools.combinations(self.scenario_relations_set, nrel):
                #solver candidates formed from
                #two relation
                solver_candidates_list = self.buildsome_solvercandidates(rel_set)
                self.solver_candidates_list += solver_candidates_list




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

        self.wisdomgraph = nx.MultiDiGraph()

        # populate self.wisdomgraph.nodes
        # a node is: (node name str, vars=set of vars)
        # nodes are state (variables known until now)
        self.add_nodes()

        #Remover
        #DiGraph().add_nodes_from() 
        #a node is an element from a dict
        #self.wisdomgraph.add_nodes_from(self.nodes_dict)

        #para obter o label de um no: "T.get_vertex(1)"

        for s in self.solver_candidates_list:
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



    def add_nodes(self):
        """
        Each node represents a set of "already known variables".

        A node is (nodename, vars=set_of_vars}

        """

        #nodes are now stores in wisdomgraph
        #self.nodes_dict = {} #dictionary: node with labels that are the set of (known) variables

        #Combinations like:
        # C = [ [], [a], [b], .., [a,b], ...,[a,b,c,d,e,f] ]
        C = Combinations( self.allvars_set )

        for varlist in C:  #sagemath is C.list():
            nname = self.node_name(varlist) #makes a str
            #OLDself.nodes_dict[nname] = set(varlist)
            self.wisdomgraph.add_node(nname,vars=set(varlist))
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
        
        #https://networkx.org/documentation/stable/reference/classes/generated/networkx.MultiDiGraph.nodes.html#networkx.MultiDiGraph.nodes
        for Inode in self.wisdomgraph.nodes(data=True):
            #for Inode_name in self.nodes_dict.keys():

            #Inode_name is a str

            #set of known variables (a node accessed by str (see node_name()) )
            #Inode = Inode[0], Inode[1] = (name, datadict)

            Ivars = Inode[1]['vars'] #set( self.nodes_dict[Inode_name] )  
            
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

                    #add_edge is from nx.MultiDiGraph()
                    self.wisdomgraph.add_edge(Inode_name,Onode_name,key=solver_candidate.solvername,sc=solver_candidate)



    def remove_edge_from_solver(self,solver_candidate):
        """
        See remove_edge_from_solver.

        Referência:

        - https://networkx.org/documentation/stable/reference/classes/multidigraph.html


        """

        edges_to_remove = [ (u,v,key) for (u, v, key) in self.wisdomgraph.edges(keys=True) if key==solver_candidate.solvername]

        self.wisdomgraph.remove_edges_from(edges_to_remove)




    def draw_wisdom_graph(self,figsize=[10,10],plot_fn=f'output_{datetime.datetime.now().strftime(r"%y%m%d-%H%M")}.pdf'):
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


    def buildall(self, number_of_given_vars=None, number_of_variants_per_exercise=None, silence=True):
        """
        Add exercises to a file.

        Input:
        - number_of_given_vars: None or positive integer.
        - number_of_variants_per_exercise: combinations of variables could make a lot of cases, this max cuts them out.

        If self.text_service.gen_method == 'challenge' it does like:

        - `buildall(no_of_given_vars= len(allvars_list) - 1) # probably the easiest`
        - `buildall(no_of_given_vars= len(allvars_list) - 2) # maybe a little more difficult`
        - etc
        - `` buildall(no_of_given_vars= 1) # probably the most difficult`

        """

        self.build_in_silence = silence

        if self.text_service.gen_method == 'challenge': 

            # Each new exercises have an increased 'number_of_given_vars': from total_vars-1 to 0.
            total_vars = len(self.allvars_list)
            for nvars in range(total_vars-1, 0, -1):
                print("="*20)
                print(f"Generate exercises with {nvars} given variables.")
                print("="*20)

                self.text_service.buildall_exercises(number_of_given_vars=nvars,
                                                     number_of_variants_per_exercise=number_of_variants_per_exercise,
                                                     silence=silence)
                
        elif self.text_service.gen_method == 'exam': 

            # All exercises have a fixed 'number_of_given_vars'
            self.text_service.buildall_exercises(number_of_given_vars=number_of_given_vars,
                                                 number_of_variants_per_exercise=number_of_variants_per_exercise,
                                                 silence=silence)

        else:

            raise


    def yield_givenvarsset_nodepathlist(self, no_of_given_vars=1):
        """
        Builds exercises from a given set of variables.

        1. An objet of type TextService is created by an author (inside a *.py file)
        2. etc
        3. A Scenario is created with all previous elements
        4. This method `buildall()` generates combinations and produces one file (samefile=True) or several files (samefile=False).

        
        An exercise is defined by:
        - givenvars_set : the known variables
        - nodepath_list : path from "ignorance" to the "knowledge" (or node of known variables?)

                
        parameters
        ==========

        - no_of_given_vars : number of known variables (search exercises with this restriction).
        

        Recall: data is in an excel file inside a TextService object. Each column a variable. Each row an exercise.


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


        # Generate all combinations of specified size
        # requested in arguments.
        C = Combinations(self.allvars_list, include_empty_set=False)

        #TODO: improve performance

        # Calcular pesos de cada set de variaveis, fazer uma lista com pesos como esta
        #d = [ [['a','b'], 5], [['q','f'], 8], [['l','p'], 5], [['a','s'],8] ]
        #d = sorted(d, key=lambda x: x[1], reverse=True)
        #print(d)
        C_weighted = [
            [var_combination, self.input_level(var_combination)] for var_combination in C
        ]

        C_weighted = sorted(C_weighted, key=lambda x: x[1]) #, reverse=True)

        # sv is a pair[ (sympy vars), input_level ]
        original_list_of_givenvars_set = [sv[0] for sv in C_weighted if len(sv[0]) == no_of_given_vars]


        #Novo
        list_of_givenvars_set  = []
        list_of_node_path_list = []

        # -----------------------------------------
        # Each tuple in "all_vars_sets" produce an exercise
        # -----------------------------------------
        for givenvars_set in original_list_of_givenvars_set:

            #
            # Discussion: when is this combination necessary?
            #
            # Creates edges from ignorance
            # to each combinations of variables
            # icomb = Combinations(givenvars_set, empty = False)
            #print(icomb)

            # Forçar solução única de partida:
            icomb =  [givenvars_set]

            for set_of_var in icomb:
                set_of_var_node = set2orderedstr(set_of_var)
                self.add_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set(set_of_var), #output set like {a} (single var)
                        set({SympyRelation(0, free_symbols=set_of_var,latex_str=f"given {set_of_var_node}")}) 
                    )
                )

            #TODO: configurar 50,50 de forma automatica
            #self.draw_wisdom_graph(figsize=(50,50))

            #ANTES: Check if has_path
            #has_a_path = nx.has_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)
                
            #AGORA: write all paths (each path is an exercise)
            if not self.build_in_silence:
                print("="*10)
                print(f"Caminhos sabendo: {givenvars_set}")
                print("="*10)

            #Shortest
            try:
                node_path_list = list(nx.shortest_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_))

                if not self.build_in_silence:
                    for node in node_path_list:
                        print(node)

                #DEBUG
                #self.debug_exercise(givenvars_set,node_path_list)

                #muito antigo
                #requestedvars_set = set(self.allvars_list) - set(givenvars_set)

                #ANTES: o que estava a funcionar
                #dataframe_iloc += 1
                #self.solverslist_answer_text = self.solverslist_build_answer_text(givenvars_set,node_path_list,silence)
                #teacher_text = self.text_service.build_one(self,givenvars_set,dataframe_iloc,node_path_list)

                #NOVO: keep for later use with yield
                list_of_givenvars_set.append(givenvars_set)
                list_of_node_path_list.append(node_path_list)


            except nx.NetworkXNoPath:
                if not self.build_in_silence:
                    #Debug
                    print("    Não há caminho!")

            
            #ALL paths
            #for path in sorted(nx.all_simple_edge_paths(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)):
            #    print(path)

            #Remove (artificial) edges
            for set_of_var in icomb:
                set_of_var_node = set2orderedstr(set_of_var)
                self.remove_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set(set_of_var), #output set like {a} (single var)
                        set({SympyRelation(0, free_symbols=set_of_var,latex_str=f"given {set_of_var_node}")}) #10 is not used
                    )
                )


        #-----------------
        # Yield mechanism
        #-----------------
        list_of_pairs = zip(list_of_givenvars_set,list_of_node_path_list)
        for pair in list_of_pairs:
            yield pair #(givenvars_set, node_path_list)

        #end of buildall()


    def debug_exercise(givenvars_set,node_path_list,silence=True):

        l = len(givenvars_set) #len_first_nodes

        print(f"Solution in {len(node_path_list)-l-1} steps.")

        solution_steps = []

        for nodepair in zip(node_path_list[l:-1], node_path_list[(l+1):]):

            #find edge
            print('-'*3)
            print(f'=>from {nodepair[0]}')
            print(f'=>to   {nodepair[1]}')
            print('-'*3)
            edges = [e for e in self.wisdomgraph.edges(nodepair[0], data="sc", keys=True) if e[1]==nodepair[1]]
            #edges = list(self.wisdomgraph.edges[nodepair[0]][nodepair[1]]) #, keys=True,))
            
            #There shoulbe be only one
            edge = edges[0]

            #Fourth element is a SolverCandidate 
            solver_candidate = edge[3]
            print("*"*10)
            print(self.wisdomgraph.nodes[nodepair[0]]['vars'])
            print(self.wisdomgraph.nodes[nodepair[1]]['vars'])
            print(solver_candidate.relations_latex())
            print("*"*10)

            #Construção de um exercício
            #solution_steps += ()

