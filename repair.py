from ai_interface import AIInterface

repair_prompt = "You are an input repairer. Your task is to fix a corrupted input based on the parser’s code, ensuring that the corrected input can be successfully parsed. Analyze both the parser’s code and the corrupted text to restore the input as accurately as possible while keeping it as close to the original as you can. Just return the fixed input without any explanations."

def repair(program,corrupted_text,backend,model):
    ai  =  AIInterface(backend,model)
    return ai.get_response(repair_prompt,"code:\n"+program+"corrupted_text:\n"+corrupted_text)