import ast
import networkx as nx
import matplotlib.pyplot as plt
import inspect
import sympy

def analyze_function(func):
    # Get the function's source code
    source = inspect.getsource(func)
    
    # Parse the AST
    tree = ast.parse(source)
    
    # Create a directed graph
    graph = nx.DiGraph()
    
    # Track variable assignments and usage
    assignments = set()
    usages = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    assignments.add(var_name)
                    # Add edges from variables used in the assignment
                    for n in ast.walk(node.value):
                        if isinstance(n, ast.Name):
                            graph.add_edge(n.id, var_name)
        
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            usages.add(node.id)
    
    # Add nodes for all variables
    all_vars = assignments.union(usages)
    for var in all_vars:
        if var not in graph:
            graph.add_node(var)
    
    return graph

def plot_variable_graph(func):
    graph = analyze_function(func)
    plt.figure(figsize=(20,20))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=300, node_color='skyblue', 
            font_size=10, font_weight='bold', arrowsize=20)
    plt.title("Variable Connections in Function")
    #plt.show()
    plt.savefig("equacoes.png")


# Example usage:
def example_function(ndiassemana,probsucesso,valory,nsemanas):

    #"Eq(disty, ndiassemana+probsucesso)",                 
    #"Eq(probvalory, ndiassemana+probsucesso+valory)",     
    #"Eq(probsemanas, ndiassemana+probsucesso+nsemanas)",  

    disty = ndiassemana+probsucesso
    probvalory = ndiassemana+probsucesso+valory
    probsemanas = ndiassemana+probsucesso+nsemanas

def example_sympy():
    from sympy import symbols, Eq

    # Define the symbols
    a, b, c = symbols('a b c')

    # Create the equation a + b = c
    equation = Eq(a + b, c)

    # Print the equation
    #print(equation)

plot_variable_graph(example_function)