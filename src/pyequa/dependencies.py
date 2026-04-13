"""
dataset: tools to make datasets and store then in csv or excel.
2026 @ Joao Pedro Cruz
"""

import ast
import inspect
import networkx as nx
import matplotlib.pyplot as plt



def make_precedence_dictionary(funname):
    """
    Docstring for make_precedence_graph
    
    :param funname: Description

    ```python
    'pfemeas': {'pmachos100'}, 
    'EE': {'n', 'pfemeas'}, 
    'Var': {'n', 'pfemeas'}, 
    'pexatamente': {'pfemeas', 'n', 'numexatamente'}, 
    'ppelomenos': {'numpelomenos', 'n', 'pfemeas'}, 
    'phiper': {'BigN', 'n', 'pfemeas'}
    ```
    """
    # Get the source code of the function
    source = inspect.getsource(funname)
    tree = ast.parse(source)
    
    # Extract function parameters (input variables)
    func_def = tree.body[0]
    params = {arg.arg for arg in func_def.args.args}
    
    # Dictionary to store dependencies
    dependencies = {}
    
    # Visit each assignment in the function
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Get the variable being assigned
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    
                    # Find all variables used in the right-hand side
                    used_vars = set()
                    for subnode in ast.walk(node.value):
                        if isinstance(subnode, ast.Name) and isinstance(subnode.ctx, ast.Load):
                            # Only include if it's a parameter or previously defined variable
                            if subnode.id in params or subnode.id in dependencies:
                                used_vars.add(subnode.id)
                    
                    dependencies[var_name] = used_vars
    
    return dependencies


def draw_graph(G_visual, node_labels, dependencies):

    #G = make_graph(make_precedence_graph(calculate))

    # Draw the graph
    #G_visual = nx.DiGraph()
    #dependencies = make_precedence_graph(calculate)

    # Rebuild the graph for visualization
    for var, deps in dependencies.items():
        G_visual.add_node(var)
        for dep in deps:
            G_visual.add_node(dep)
            G_visual.add_edge(dep, var)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G_visual, k=2, iterations=50)

    # Use the returned dictionary for labels
    nx.draw(G_visual, pos, with_labels=True, labels=node_labels, node_color='lightblue', 
            node_size=3000, font_size=10, font_weight='bold',
            arrows=True, arrowsize=20, edge_color='gray', 
            arrowstyle='->', connectionstyle='arc3,rad=0.1')
    plt.title("Variable Dependency Graph (Topological Levels)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('variable_dependencies.png', dpi=300, bbox_inches='tight')


def make_graph(dependencies):
    """
    Create a directed graph from variable dependencies.
    
    :param dependencies: Dictionary mapping variables to their dependencies
                        Example: {'pfemeas': {'pmachos100'}, 'EE': {'n', 'pfemeas'}}
    :return: NetworkX DiGraph where edges point from dependencies to dependents
             Nodes are labeled: 1 for source nodes (no inputs), 
             other nodes labeled with shortest path from source nodes
    
    Example:
        If 'EE': {'n', 'pfemeas'}, creates edges: n -> EE and pfemeas -> EE
    """
    G = nx.DiGraph()
    
    # Add all nodes (both dependent and dependency variables)
    for var, deps in dependencies.items():
        G.add_node(var)
        for dep in deps:
            G.add_node(dep)
    
    # Add edges from dependencies to dependent variables
    for var, deps in dependencies.items():
        for dep in deps:
            G.add_edge(dep, var)
    
    # Find source nodes (nodes with no input edges)
    source_nodes = [node for node in G.nodes() if G.in_degree(node) == 0]
    
    # Label source nodes with 1
    for node in source_nodes:
        G.nodes[node]['label'] = 1
    
    # For other nodes, compute shortest path from any source node
    for node in G.nodes():
        if node not in source_nodes:
            min_path_length = float('inf')
            for source in source_nodes:
                try:
                    path_length = nx.shortest_path_length(G, source, node)
                    min_path_length = min(min_path_length, path_length)+1
                except nx.NetworkXNoPath:
                    # No path exists from this source to this node
                    pass
            
            if min_path_length != float('inf'):
                G.nodes[node]['label'] = min_path_length
    
    # Traverse the graph and output node information
    #Debug
    #print("\n--- Graph Traversal: Node Names and Labels ---")
    node_labels = {}
    for node in sorted(G.nodes(), key=lambda n: G.nodes[n].get('label', float('inf'))):
        label = G.nodes[node].get('label', 'undefined')
        node_labels[node] = label
        #Debug
        #print(f"{node}: {label}")

    #Debug
    #print("--- End of Traversal ---\n")
    
    draw_graph(G, node_labels, dependencies)

    return node_labels



def make_var_declarations(funname):
    """
    Docstring for make_var_declarations
    
    :param funname: Description

    Example:
    ```python    
    variable_attributes = {
        'BigN': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
        'pmachos100': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
        'n': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
        'pfemeas': {'type': 'numerical', 'tol': 0.001,  'givenvarlevel': 2},
        'EE': {'type': 'numerical', 'tol': 0.001,  'givenvarlevel': 2},
        'Var': {'type': 'numerical', 'tol': 0.001,  'givenvarlevel': 2},
        'numexatamente': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
        'pexatamente': {'type': 'numerical', 'tol': 0.001,  'givenvarlevel': 2},
        'numpelomenos': {'type': 'numerical', 'tol': 0,  'givenvarlevel': 1},
        'ppelomenos': {'type': 'numerical', 'tol': 0.001,  'givenvarlevel': 2},
        'phiper': {'type': 'numerical', 'tol': 0.001,  'givenvarlevel': 2},
    }
        'BigN': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1}
        'pmachos100': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1}
        'n': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1}
        'numexatamente': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1}
        'numpelomenos': {'type': 'numerical', 'tol': 0, 'givenvarlevel': 1}
        'pfemeas': {'type': 'numerical', 'tol': 0.01, 'givenvarlevel': 1}
        'EE': {'type': 'numerical', 'tol': 0.01, 'givenvarlevel': 1}'Var': {'type': 'numerical', 'tol': 0.01, 'givenvarlevel': 1}
        'pexatamente': {'type': 'numerical', 'tol': 0.01, 'givenvarlevel': 1}
        'ppelomenos': {'type': 'numerical', 'tol': 0.01, 'givenvarlevel': 1}
        'phiper': {'type': 'numerical', 'tol': 0.01, 'givenvarlevel': 1}
    ```
    """

    precedence_dictionary = make_precedence_dictionary(funname)

    node_labels = make_graph(precedence_dictionary)

    print(node_labels)

    print("variable_attributes = {")
    result = funname()
    var_types = {}
    for var_name, var_value in result.items():
        var_types[var_name] = type(var_value).__name__
        if 'int' in var_types[var_name]:
            print(f"    '{var_name}': {{'type': 'numerical', 'tol': 0, 'givenvarlevel': {node_labels[var_name]}}},")
        elif 'float' in var_types[var_name]:
            print(f"    '{var_name}': {{'type': 'numerical', 'tol': 0.01, 'givenvarlevel': {node_labels[var_name]}}},")
        else:
            print(f"    '{var_name}': {{'type': 'mutichoice', 'givenvarlevel': {node_labels[var_name]}}},")
    print("}")

    return var_types


