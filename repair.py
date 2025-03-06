from ai_interface import AIInterface

repair_prompt = """You are an input repairer. Your task is to fix a corrupted input based on the parser’s code, ensuring that the corrected input can be successfully parsed. Analyze both the parser’s code and the corrupted text to restore the input as accurately as possible while keeping it as close to the original as you can. 
PLEASE DO NOT EXPLAIN,
PLEASE DO NOT ADD OTHER FORMAT, 
PLEASE DO NOT CHANGE THE PARSER'S CODE ONLY FIXED INPUT, YOU NEED TO FIX CORRUPTED INPUT LIKE: asfase.
The final reture should be like this:
abcd"""

def repair(program,corrupted_text,backend,model):
    ai  =  AIInterface(backend,model)
    return ai.get_response(repair_prompt,"parser code:\n"+program+"corrupted_input:\n"+corrupted_text)