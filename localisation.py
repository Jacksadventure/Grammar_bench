from ai_interface import AIInterface

repair_prompt = """You are an localisation expert. Your task is to localize position of corrupted input and funtion name in the parser based on the parser’s code. You should only return 1 function name and when counting the position of corrupted input, you should start from 0. 
PLEASE DO NOT EXPLAIN,
PLEASE DO NOT ADD OTHER FORMAT, 
Please return result in this format:
{
    "function_name": "parse_A",
    "corrupted_input_position": 5
}
Please do not add markdown notation like ```json
"""

def localise(program,corrupted_text,backend,model):
    ai  =  AIInterface(backend,model)
    return ai.get_response(repair_prompt,"parser code:\n"+program+"corrupted_input:\n"+corrupted_text)