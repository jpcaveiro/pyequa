"""
 wisdomgraph: exercises based on environments 
 2019 @ jpcaveiro@github
 SageMath
 Using python standard libs as much as possible

 MultiDIGraph from networkx:
 https://networkx.org/documentation/stable/reference/classes/multidigraph.html
"""


import itertools
import numbers
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import numpy as np
from sympy import Eq, Symbol, latex, parse_expr


#from slugify import slugify
#from sage.all import *


def sortedsymbols(symbols_iterable):
    """Return SymPy symbols sorted by their string names.

    Sorting by ``str`` avoids SymPy's expression-ordering semantics, which
    don't represent alphabetical ordering of symbol names.
    """
    return sorted(symbols_iterable,key=Symbol.__str__)


#def symbolslug(s):
#    return slugify(s.__str__())



def Combinations(someset, include_empty_set = True):
    """
    Return all combinations of the input values as tuples.

    Args:
        someset: Iterable of values to combine.
        include_empty_set: If true, include the empty tuple as the first
            combination.

    Returns:
        A list containing combinations from size zero (or one) through the
        full input size.
    """

    list_of_sets = []

    if include_empty_set:
        start = 0  #itertools.combinations(someset, 0) produce empty set
    else:
        start = 1

    # Version 1
    for i in range(start,len(someset)+1):
        # Calculate all combinations of size i
        for combo in itertools.combinations(someset, i):
            list_of_sets.append(combo)
            #print(combo)

    # Version 2
    #for i in range(start,len(someset)+1):
    #    # Add all combinations of size i
    #    list_of_sets.append(list(itertools.combinations(someset, i)))



    return list_of_sets



def Combinations_of_givensize(someset, givensize):
    """Return all fixed-size combinations of the input values.

    Args:
        someset: Iterable of values to combine.
        givensize: Number of values in each combination.

    Returns:
        A list of tuples, each containing ``givensize`` values.
    """

    # Version 1
    list_of_sets = []
    for combo in itertools.combinations(someset, givensize):
        list_of_sets.append(combo)

    # Version 2
    #list_of_sets = list(itertools.combinations(someset, givensize))

    return list_of_sets


def set2orderedstr(someset):
    """Return a stable string representation of a collection of symbols.

    Symbol names are sorted before conversion, so the result is independent
    of the collection's iteration order.
    """

    #return str(sorted([str(s) for s in someset]))
    return str(sorted([s.name for s in someset]))


def float2int(value):
    """Convert a finite integral numeric value to ``int`` when possible.

    Non-numeric values, non-finite numbers and values with a fractional part
    are returned unchanged.
    """

    if isinstance(value, (numbers.Number, np.number)) and np.isfinite(value) and float(value).is_integer():
        return int(value)
    else:
        return value

    
def join_varnames(varlist):
    """Join symbol names into a single string in alphabetical order."""
    # ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    # 33538048  165.962    0.000 2439.667    0.000 scenario.py:94(join_varnames)  
    # Version 1
    # return "".join( sorted( [str(v) for v in varlist] ) )   

    # Version 2
    # 33538048   30.249    0.000   53.720    0.000 scenario.py:94(join_varnames)
    # return "".join( sorted( [v.name for v in varlist] ) )   

    # Version 3
    x = [v.name for v in varlist]
    list.sort(x)
    return "".join( x )   







class SympyRelation:
    """Pair a SymPy relation with its free symbols and LaTeX representation.

    ``free_symbols`` and ``latex_str`` can be supplied to override the values
    inferred from the relation.
    """
    
    def __init__(self,sympyrelation,free_symbols=None,latex_str="", input_is_str=False):
        """Create a relation wrapper.

        Args:
            sympyrelation: SymPy relation/expression, or a string when
                ``input_is_str`` is true.
            free_symbols: Optional explicit set of symbols used by the
                relation.
            latex_str: Optional pre-rendered LaTeX to use for output.
            input_is_str: Parse ``sympyrelation`` as a SymPy expression when
                true.
        """
        
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
        """Return the relation's LaTeX representation."""
        return self.latex_str
    
    def __repr__(self):
        """Return a constructor-like representation of this wrapper."""
        return f"SympyRelation({self.sympyrelation},{self.free_symbols},{self.latex_str})"

SR = SympyRelation        



class SolverCandidate:
    """Describe a possible transition from known to solvable variables.

    A candidate records its input variables, output variables and supporting
    relations. It represents a proposed route; it does not itself prove that
    the relations can be solved for the outputs.
    """


    def __init__(self,input_set,output_set,relations_set):
        """Create a solver candidate from variable sets and relations.

        Args:
            input_set: Variables assumed to be known before applying the
                candidate.
            output_set: Variables the candidate may determine.
            relations_set: Relations supporting this transition.
        """

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
        """Return the candidate's relations joined as LaTeX text."""
        return '\n\n'.join([r.latex_str for r in self.signature['relations_set']])



class Scenario:
    """Build and query the variable-knowledge graph for an exercise.

    Relations are converted into solver candidates and graph transitions.
    Each graph node represents the variables known at that point; a path from
    ``ignorance`` to ``knowledge`` describes one solution route.
    """

    _IGNORANCE_NODE_NAME_ = 'ignorance'
    _KNOWLEDGE_NODE_NAME_ = 'knowledge'

    def __init__(self, pyequa_instance, scenario_relations, text_service, list_of_number_of_relations_at_once=None):
        """Create solver candidates and the knowledge graph.

        Args:
            pyequa_instance: Parent :class:`PyEqua` instance, used for
                exercise paths and configuration.
            scenario_relations: Iterable of :class:`SympyRelation` instances
                or SymPy expression strings.
            text_service: Service that supplies variable metadata and
                generation settings. The scenario is attached to this
                service.
            list_of_number_of_relations_at_once: Relation counts to combine
                when building solver candidates. Defaults to every count from
                one through the total number of relations.
        """

        #pyequa_instance helps in filesystem, etc.
        self.pyequa_instance = pyequa_instance

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
        self.config = text_service.config
        
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


    def input_level(self, var_combination, reverse=False):
        """Sum the configured given-variable levels for a combination.

        Variables without an explicit ``givenvarlevel`` contribute one.
        ``reverse=True`` negates the total, allowing the same sort operation
        to order combinations from higher to lower levels.
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

        if reverse:
            return -input_level_sum
        else:
            return input_level_sum


    def buildsome_solvercandidates(self, rel_set): 
        """
        Propose input-to-output transitions supported by a relation set.

        For each combination of output variables common to all relations,
        creates a :class:`SolverCandidate` whose inputs are the remaining
        variables used by the relations. Candidates describe possible
        transitions; this method does not verify that the relations are
        algebraically solvable for those outputs.

        Args:
            rel_set: Non-empty iterable of :class:`SympyRelation` objects.

        Returns:
            A list of proposed :class:`SolverCandidate` instances.

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
        """Populate ``solver_candidates_list`` from relation combinations.

        For each count in ``list_of_number_of_relations_at_once``, combines
        that many scenario relations and asks :meth:`buildsome_solvercandidates`
        for the possible input-to-output transitions.
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
        """Build ``wisdomgraph`` from the solver candidates.

        Nodes represent known-variable sets, and directed edges represent
        candidates that add one or more variables to the known set.
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
        """Return the graph label for a set of symbols.

        The empty set and the complete set use the special labels
        ``ignorance`` and ``knowledge`` respectively.
        """

        nname = join_varnames(varlist)   

        #nomes especiais

        #TODO: this special names into default_config.yaml
        if nname=='':
            nname = Scenario._IGNORANCE_NODE_NAME_ #'ignorancia'
        elif nname == self.node_knowledge_name:
            nname = Scenario._KNOWLEDGE_NODE_NAME_ #'conhecimento'

        #Debug:
        #print( "node_name=", node_name([f,a]) )

        return nname



    def add_nodes(self):
        """Add one graph node for each subset of scenario variables."""

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
        """Remove all graph edges created from the supplied solver candidate.

        Args:
            solver_candidate: Candidate whose solver name identifies the
                edges to remove.
        """

        edges_to_remove = [ (u,v,key) for (u, v, key) in self.wisdomgraph.edges(keys=True) if key==solver_candidate.solvername]

        self.wisdomgraph.remove_edges_from(edges_to_remove)




    def draw_wisdom_graph(self,plot_fn=f'output_{datetime.datetime.now().strftime(r"%y%m%d-%H%M")}.pdf', figsize=[10,10]):
        """Draw the knowledge graph and save it in the exercise folder.

        Args:
            plot_fn: Output filename, relative to the exercise folder.
            figsize: Matplotlib figure size as ``(width, height)`` in inches.
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
        #nx.draw_networkx_edge_labels(G, pos=pos_dic, edge_labels=edge_labels_dict)

        #from .config import PYEQUA_PROJECT_ROOT
        from pathlib import Path


        plt.savefig(self.pyequa_instance.exercise_folder / Path(plot_fn))


    def yield_givenvarsset_nodepathlist_from_varset(self, givenvars_set=None):
        """Yield a solution path for the supplied set of known variables.

        Args:
            givenvars_set: Iterable of SymPy symbols treated as already known.

        Yields:
            Pairs of ``(givenvars_set, node_path_list)`` for reachable paths.
        """
        list_of_list_of_givenvars_set = [ list(givenvars_set) ]
        return self.yield_givenvarsset_nodepathlist(list_of_list_of_givenvars_set)



    def yield_givenvarsset_nodepathlist_from_number(self, number_of_given_vars=None, reverse=False):
        """Yield paths for every combination of a specified size.

        Combinations are ordered by their summed ``givenvarlevel`` metadata.

        Args:
            number_of_given_vars: Number of variables in each givens
                combination.
            reverse: Reverse each combination's input-level score before
                sorting, useful for ordering higher-level variables first.

        Yields:
            Pairs of ``(givenvars_set, node_path_list)`` for reachable paths.
        """

        # Generate all combinations of specified size
        C = Combinations_of_givensize(self.allvars_list, number_of_given_vars)

        #TODO: improve performance

        # Calcular pesos de cada set de variaveis, fazer uma lista com pesos como esta
        #d = [ [['a','b'], 5], [['q','f'], 8], [['l','p'], 5], [['a','s'],8] ]
        #d = sorted(d, key=lambda x: x[1], reverse=True)
        #print(d)
        C_weighted = [
            [var_combination, self.input_level(var_combination, reverse)] for var_combination in C
        ]

        C_weighted = sorted(C_weighted, key=lambda x: x[1]) #, reverse=True)

        # sv is a pair[ (sympy vars), input_level ]
        #list_of_list_of_givenvars_set = [sv[0] for sv in C_weighted if len(sv[0]) == number_of_given_vars]
        list_of_list_of_givenvars_set = [sv[0] for sv in C_weighted] #Not needed: if len(sv[0]) == number_of_given_vars]

        return self.yield_givenvarsset_nodepathlist(list_of_list_of_givenvars_set)



    def yield_givenvarsset_nodepathlist(self, list_of_list_of_givenvars_set=None):
        """
        Find a shortest knowledge path for each requested set of givens.

        Each supplied set is temporarily connected to the ``ignorance`` node;
        sets with no route to ``knowledge`` are skipped.

        Args:
            list_of_list_of_givenvars_set: Iterable of variable collections,
                one collection for each requested givens set.

        Yields:
            Pairs of ``(givenvars_set, node_path_list)`` for reachable sets.

        """

        assert list_of_list_of_givenvars_set

        #Novo
        list_of_givenvars_set  = []
        list_of_node_path_list = []

        # -----------------------------------------
        # Each set in list_of_list_of_givenvars_set produce an exercise
        # -----------------------------------------
        for givenvars_set in list_of_list_of_givenvars_set:
            #TODO: givenvars_set should be changed to givenvars_list
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
            if self.config['debug']:
                print("="*10)
                print(f"Caminhos sabendo: {givenvars_set}")
                print("="*10)

            #Shortest
            try:
                node_path_list = list(nx.shortest_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_))

                if self.config['debug']:
                    for node in node_path_list:
                        print(node)

                #DEBUG
                #self.debug_exercise(givenvars_set,node_path_list)

                #muito antigo
                #requestedvars_set = set(self.allvars_list) - set(givenvars_set)

                #ANTES: o que estava a funcionar
                #dataframe_iloc += 1
                #self.solverslist_answer_text = self.solverslist_build_answer_text(givenvars_set,node_path_list)
                #teacher_text = self.text_service.build_one(self,givenvars_set,dataframe_iloc,node_path_list)

                #NOVO: keep for later use with yield
                list_of_givenvars_set.append(givenvars_set)
                list_of_node_path_list.append(node_path_list)


            except nx.NetworkXNoPath:
                
                if self.config['debug']:
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
        list_of_pairs = zip(list_of_givenvars_set, list_of_node_path_list)
        for pair in list_of_pairs:
            yield pair #(givenvars_set, node_path_list)

        #end of buildall()


    def debug_exercise(givenvars_set,node_path_list):

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
