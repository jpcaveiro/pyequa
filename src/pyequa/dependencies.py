"""
dataset: tools to make datasets and store then in csv or excel.
2026 @ Joao Pedro Cruz
"""

import ast
import inspect
import networkx as nx
import matplotlib.pyplot as plt



def extract_names_from_target(target):
    """Collect names from a simple, tuple or list assignment target.

    Args:
        target: An ``ast.Name``, ``ast.Tuple`` or ``ast.List`` node.

    Returns:
        Names in source order. Other AST node types produce an empty list.
    """
    if isinstance(target, ast.Name):
        return [target.id]
    elif isinstance(target, (ast.Tuple, ast.List)):
        names = []
        for elt in target.elts:
            names.extend(extract_names_from_target(elt))
        return names
    return []


def make_precedence_dictionary(funname):
    """
    Infer variable dependencies by inspecting a function's assignments.

    Function parameters and names assigned in the function become dictionary
    keys. Each value is the set of recognized parameters or earlier
    assignments used by that assignment. This is a static approximation based
    on the function's source code, not runtime dependency tracing.

    Args:
        funname: Function object whose source should be analyzed. Its source
            must be available to :func:`inspect.getsource`.

    Returns:
        A mapping from variable names to sets of dependency names. Parameters
        and assignments with no recognized dependencies include the sentinel
        string ``"could not get relations"``.
    """
    # Get the source code of the function
    source = inspect.getsource(funname)
    tree = ast.parse(source)
    
    # Extract function parameters (input variables)
    func_def = tree.body[0]
    params = {arg.arg for arg in func_def.args.args}
    
    # Dictionary to store dependencies
    # start with params related to empty set
    _MESSAGE_ = 'could not get relations'
    dependencies = {arg.arg: {_MESSAGE_} for arg in func_def.args.args}
    
    # Visit each assignment in the function
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Get the variable being assigned
            for target in node.targets:
                # Handle simple name assignment: x = expr
                if isinstance(target, ast.Name):
                    var_name = target.id
                    
                    # Find all variables used in the right-hand side
                    used_vars = {_MESSAGE_} #set()
                    for subnode in ast.walk(node.value):
                        if isinstance(subnode, ast.Name) and isinstance(subnode.ctx, ast.Load):
                            # Only include if it's a parameter or previously defined variable
                            if subnode.id in params or subnode.id in dependencies:
                                used_vars.add(subnode.id)
                    
                    dependencies[var_name] = used_vars
                
                # Handle tuple/list unpacking: x1, x2, ... = expr1, expr2, ...
                elif isinstance(target, (ast.Tuple, ast.List)):
                    target_names = extract_names_from_target(target)
                    
                    # If RHS is also a tuple/list, match element-wise
                    if isinstance(node.value, (ast.Tuple, ast.List)):
                        for i, var_name in enumerate(target_names):
                            used_vars = {_MESSAGE_} #set()
                            if i < len(node.value.elts):
                                value_elem = node.value.elts[i]
                                for subnode in ast.walk(value_elem):
                                    if isinstance(subnode, ast.Name) and isinstance(subnode.ctx, ast.Load):
                                        if subnode.id in params or subnode.id in dependencies:
                                            used_vars.add(subnode.id)
                            dependencies[var_name] = used_vars
                    else:
                        # RHS is a single expression (e.g., function call)
                        used_vars = {_MESSAGE_} #set()
                        for subnode in ast.walk(node.value):
                            if isinstance(subnode, ast.Name) and isinstance(subnode.ctx, ast.Load):
                                if subnode.id in params or subnode.id in dependencies:
                                    used_vars.add(subnode.id)
                        for var_name in target_names:
                            dependencies[var_name] = used_vars
    
    return dependencies


def draw_graph(G_visual, node_labels, dependencies):
    """Draw a dependency graph and save it as ``variable_dependencies.png``.

    Args:
        G_visual: NetworkX graph to populate and draw.
        node_labels: Mapping of node names to display labels.
        dependencies: Mapping from each variable to its dependency names.
    """

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
    Create and draw a directed graph from a dependency mapping.

    Each edge points from an input/dependency to the variable that uses it.
    Source nodes receive level 1; reachable dependent nodes receive a level
    based on their shortest path from a source. The graph is also saved by
    :func:`draw_graph` as ``variable_dependencies.png`` in the current
    working directory.

    Args:
        dependencies: Mapping from each variable to a set of dependencies.

    Returns:
        A mapping from node names to their calculated display levels.
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



def var_declarations(funname):
    """
    Call a zero-argument function and propose pyequa variable metadata.

    The function's returned mapping supplies the variable names and example
    values; inferred dependency levels are used for ``givenvarlevel``. A
    dependency graph image is saved as a side effect.

    Args:
        funname: Zero-argument function returning a mapping of variable names
            to representative values.

    Returns:
        A pair ``(declarations, value_types)``. ``declarations`` is Python
        source text for a ``variable_attributes`` mapping, and ``value_types``
        maps each variable name to the runtime type name of its example value.
    """

    precedence_dictionary = make_precedence_dictionary(funname)

    node_labels = make_graph(precedence_dictionary)

    #print(node_labels)

    var_str = "variable_attributes = {\n"
                                
    result = funname()
    var_dict = dict()
    for var_name, var_value in result.items():
        var_dict[var_name] = type(var_value).__name__
        if 'int' in var_dict[var_name]:
            var_str += f"    '{var_name}': {{'type': 'numerical', 'tol': 0, 'givenvarlevel': {node_labels[var_name]}}},\n"
        elif 'float' in var_dict[var_name]:
            var_str += f"    '{var_name}': {{'type': 'numerical', 'tol': 0.01, 'givenvarlevel': {node_labels[var_name]}}},\n"
        else:
            var_str += f"    '{var_name}': {{'type': 'mutichoice', 'givenvarlevel': {node_labels[var_name]}}},\n"
    var_str += "}\n"

    return var_str, var_dict


def suggest_declarations(funname):
    """Print suggested variable metadata and relation declarations.

    Args:
        funname: Zero-argument function returning representative variable
            values. Its source is inspected to infer dependencies.
    """

    var_str, _ = var_declarations(funname) #_ is var_dict
    print(var_str)

    pred_dict = make_precedence_dictionary(funname)
    pred_str = "scenario_relations = {\n"

    for k in pred_dict.keys():

        eq_str = f"   'Eq({k}, " + " + ".join(pred_dict[k]) + ")',\n"
        pred_str += eq_str

    pred_str += "}\n"

    print(pred_str)

