from ai_interface import AIInterface
from ultility import remove_markdown_tags,remove_think_tags

from transformers import RobertaTokenizer

tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

repair_prompt = """You are an localisation expert. Your task is to localize position of corrupted input and funtion name in the parser based on the parser’s code. You should only return 1 function name and when counting the position of corrupted input, you should start from 0. 
PLEASE DO NOT EXPLAIN,
PLEASE DO NOT ADD OTHER FORMAT, 
Please return result in this format:
{
    "function_name": "parse_A"
}
Please do not add markdown notation like ```json
"""

program_localisation_prompt = """You are a patch generator. Given the corrupted parser code annotated with line numbers and the original grammar, output a unified diff patch to fix the parser so it matches the grammar. Only output the patch in standard unified diff format, without explanations or extra text.

Example:
@@ -12,7 +12,7 @@ def parse_X():
-    old code line
+    new code line

PLEASE DO NOT ADD MARKDOWN TAG LIKE```diff, ``` IN YOUR RESPONSE.
"""

def localise_program_input(program, corrupted_text, backend, model):
    ai = AIInterface(backend, model)
    return ai.get_response(
        repair_prompt,
        "parser code:\n" + program + "\ncorrupted_input:\n" + corrupted_text
    )

def localise_program(program, grammar, backend, model):
    ai = AIInterface(backend, model)
    # Annotate parser code with line numbers for AI reference
    annotated = [f"{i}: {line}" for i, line in enumerate(program.splitlines(), start=1)]
    prompt_input = (
        "parser code with line numbers:\n"
        + "\n".join(annotated)
        + "\ngrammar:\n"
        + grammar
    )
    # Call the AI interface and clean the returned text while preserving token usage
    resp = ai.get_response(program_localisation_prompt, prompt_input)
    text = remove_markdown_tags(remove_think_tags(resp.response_text))
    resp.response_text = text
    return resp
