import ast
import sys

generate_patch_prompt = """
You are a patch generator 
"""

def replace_function_ast_in_file(original_file: str, new_function_code: str, func_name: str):
    """
    Replaces the function named `func_name` in `original_file` with
    the new function code given by `new_function_code` (a string).
    Overwrites the original file without creating a backup.
    """

    # 1. Read and parse the original  
    with open(original_file, "r", encoding="utf-8") as f:
        original_code = f.read()
    original_ast = ast.parse(original_code)

    # 2. Parse the new function code
    try:
        new_func_ast = ast.parse(new_function_code)
    except SyntaxError as e:
        print("Failed to parse new function code. Please check for syntax errors.")
        print(f"Error: {e}")
        sys.exit(1)

    # 3. Locate the function definition in the new function code
    new_func_def = None
    for node in ast.iter_child_nodes(new_func_ast):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            new_func_def = node
            break

    if not new_func_def:
        print(f"No function named '{func_name}' found in the new function code.")
        sys.exit(1)

    # 4. Create a NodeTransformer to replace the old function with the new one
    class FunctionReplacer(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name == func_name:
                # Replace with the new function definition
                return new_func_def
            return self.generic_visit(node)

    replacer = FunctionReplacer()
    updated_ast = replacer.visit(original_ast)

    # 5. Convert the modified AST back to source code
    try:
        updated_code = ast.unparse(updated_ast)
    except Exception as e:
        print("Error during unparse. Possibly Python version < 3.9 or AST issue.")
        print(f"Error: {e}")
        sys.exit(1)

    # 6. Overwrite the original file
    with open(original_file, "w", encoding="utf-8") as f:
        f.write(updated_code)

    print(f"Successfully replaced function '{func_name}' in '{original_file}'.")