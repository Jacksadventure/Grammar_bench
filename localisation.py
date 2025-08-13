from ai_interface import AIInterface
from ultility import remove_markdown_tags,remove_think_tags



repair_prompt = """You are an localisation expert. Your task is to localize position of corrupted input and funtion name in the parser based on the parser’s code. You should only return 1 function name and when counting the position of corrupted input, you should start from 0. 
PLEASE DO NOT EXPLAIN,
PLEASE DO NOT ADD OTHER FORMAT, 
Please return result in this format:
{
    "function_name": "parse_A"
}
Please do not add markdown notation like ```json
"""

program_localisation_prompt = """You are a patch generator. Your task is to generate a patch for the parser code to fix the issue that it cannot parse the input.
User has identified that the paser() function contains a bug that prevents it from parsing the input correctly.
Original code:
{original_code}
issue:
According to the grammar, this parser should accept the input:
{failing_test_cases}

Please return the patch in python, without explanations or extra text.
example of patch:

def parse(inp):
    global tokens, pos
    tokens = list(inp.strip())
    pos = 0
    while pos < len(tokens) and (tokens[pos] == 'b'):
        match('b')
    if pos < len(tokens):
        la = tokens[pos]
        if la == '*':
            match('*')
            # standard alts for <B>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <B>')
            else:
                la = tokens[pos]
                if la == '7':
                    match('7')
                    match(';')
                elif la == 'm':
                    match('m')
                    match('/')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <B>')
        elif True:  
            pass
    if pos < len(tokens):
        raise ParseError(f'Extra input at end: {"".join(tokens[pos:])}')
    print("Input accepted.")

PLEASE MAKE ONLY MINIMAL CHANGES TO THE CODE.
PLEASE DON'T MODIFY ERROR HANDLING. 
please Don't add annotations like ```python
Please ONLY return parse(inp) function.
"""

patch_refiner_patch_grammar = """
Original code:
{original_code}

Patch:
{patch_text}

compilation error message:
{error_message}

You are a patch refiner. Your task is to refine the patch to ensure it can be applied in original code with intention without introducing new compilation error.
Please return the refined patch in standard unified diff format, without explanations or extra text.
PLEASE DO NOT ADD MARKDOWN TAG LIKE ```diff``` or ```python``` IN YOUR RESPONSE(***IMPORTANT***).
"""


patch_refiner_patch_logic = """
Original buggy code:
{original_code}

original issue:
According to the grammar, this parser should accept the input: 
{failing_test_cases}

problematic patch:
{patch_text}

You are a patch refiner. The buggy pathch is failed to fix the original code for fixing the original issue.
Your task is to refine the patch to ensure it correctly fixes the original code without introducing new errors.
Please return the refined patch in standard unified diff format, without explanations or extra text.
PLEASE DO NOT ADD MARKDOWN TAG LIKE ```diff``` ```python```IN YOUR RESPONSE(***IMPORTANT***).
"""

# patch_refiner_format = """
# Original code:
# {original_code}

# patch:
# {patch_text}

# You are a patch refiner. Your task is to refine the patch to ensure it can be applied in original code with intention without introducing new errors.
# You should especially make sure that the patch indicates the correct line numbers in the original code.
# PLEASE DO NOT ADD MARKDOWN TAG LIKE ```diff``` IN YOUR RESPONSE(***IMPORTANT***).
# """


def localise_program_input(program, corrupted_text, backend, model):
    ai = AIInterface(backend, model)
    return ai.get_response(
        repair_prompt,
        "parser code:\n" + program + "\ncorrupted_input:\n" + corrupted_text
    )

def localise_program(program, examples, backend, model):
    ai = AIInterface(backend, model)
    # Avoid .format because the template contains braces in example code (e.g., {la!r})
    # which would trigger KeyError during str.format. Do targeted replacement instead.
    failing_joined = "\n".join(examples)
    prompt = program_localisation_prompt
    prompt = prompt.replace("{original_code}", program)
    prompt = prompt.replace("{failing_test_cases}", failing_joined)
    resp = ai.get_response(program_localisation_prompt, prompt)
    text = remove_markdown_tags(remove_think_tags(resp.response_text))
    resp.response_text = text
    return resp

def refine_patch_grammar(original_code, patch_text, error_message, backend, model):
    ai = AIInterface(backend, model)
    prompt = patch_refiner_patch_grammar.format(
        original_code=original_code,
        patch_text=patch_text,
        error_message=error_message
    )

    resp = ai.get_response(prompt, "")
    text = remove_markdown_tags(remove_think_tags(resp.response_text))
    resp.response_text = text
    return resp

def refine_patch_logic(original_code, failing_test_cases, patch_text, backend, model):
    ai = AIInterface(backend, model)
    prompt = patch_refiner_patch_logic.format(
        original_code=original_code,
        failing_test_cases="\n".join(failing_test_cases.splitlines()),
        patch_text=patch_text
    )
    resp = ai.get_response(prompt, "")
    text = remove_markdown_tags(remove_think_tags(resp.response_text))
    resp.response_text = text
    return resp

# def refine_patch_format(original_code, patch_text, backend, model):
#     ai = AIInterface(backend, model)
#     annotated = [f"{i} {line}" for i, line in enumerate(original_code.splitlines(), start=1)]
#     prompt = patch_refiner_format.format(
#         original_code="\n".join(annotated),
#         patch_text=patch_text
#     )
#     resp = ai.get_response(prompt, "")
#     text = remove_markdown_tags(remove_think_tags(resp.response_text))
#     resp.response_text = text
#     return resp
