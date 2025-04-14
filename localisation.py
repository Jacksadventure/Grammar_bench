from ai_interface import AIInterface

repair_prompt = """You are an localisation expert. Your task is to localize position of corrupted input and funtion name in the parser based on the parser’s code. You should only return 1 function name and when counting the position of corrupted input, you should start from 0. 
PLEASE DO NOT EXPLAIN,
PLEASE DO NOT ADD OTHER FORMAT, 
Please return result in this format:
{
    "function_name": "parse_A"
}
Please do not add markdown notation like ```json
"""

program_localisation_prompt = """You are an localisation expert. Your task is to localize the corrupted function in the parser based on the parser’s code. You should only return a function name.that caused the inconsistency between the code of parser and input, and also give a correct version of that function" \
PLEASE DO NOT EXPLAIN,
PLEASE DO NOT ADD OTHER FORMAT, 
Please return result in this format:
{
    "function_name": "parse_A"
    "correct_version": "def parse_A():\\n  ..."
}
Please do not add markdown notation like ```json!!!
Plsease make sure the function name is correct and the function is complete, and the function should be a valid python code.
Please make sure that responce is a valid json format, using \\n if necessary."""
def localise_program_input(program,corrupted_text,backend,model):
    ai  =  AIInterface(backend,model)
    return ai.get_response(repair_prompt,"parser code:\n"+program+"corrupted_input:\n"+corrupted_text)

def localise_program(program,input,backend,model):
    ai  =  AIInterface(backend,model)
    return ai.get_response(program_localisation_prompt,"parser code:\n"+program+"input:\n"+input) 