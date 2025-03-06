import ast
import sys
from collections import defaultdict

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.call_graph = defaultdict(set)  # Store function call relationships
        self.current_function = None  # Track the currently visited function
    
    def visit_FunctionDef(self, node):
        """Visit function definitions"""
        self.current_function = node.name
        self.generic_visit(node)  # Recursively visit the function body
        self.current_function = None
    
    def visit_Call(self, node):
        """Visit function calls"""
        if isinstance(node.func, ast.Name):  # Direct function call
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):  # Method call
            func_name = node.func.attr
        else:
            func_name = None
        
        if self.current_function and func_name:
            self.call_graph[self.current_function].add(func_name)
        
        self.generic_visit(node)  # Recursively visit child nodes

def analyze_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename)
    
    visitor = FunctionCallVisitor()
    visitor.visit(tree)

    print("Function Call Relationships:")
    for caller, callees in visitor.call_graph.items():
        print(f"{caller} calls -> {', '.join(callees)}")
