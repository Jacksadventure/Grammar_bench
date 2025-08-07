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

program_localisation_prompt = """You are a patch generator. Given the corrupted parser code annotated with line numbers and a few examples of inputs that the parser currently fails on which are supposed to pass, output a unified diff patch to fix the parser so it correctly handles those inputs. Only output the patch in standard unified diff format, without explanations or extra text.

Example:
Corrupted parser code with line numbers:

1  import sys
2
3  tokens = []
4  pos = 0
5
6  def error(msg):
7      print("Parse error:", msg)
8      sys.exit(1)
9
10  def match(expected):
11      global pos, tokens
12      if pos < len(tokens) and tokens[pos].startswith(expected):
13          pos += 1
14      else:
15          error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))
16
17  def parse_M():
18      global pos, tokens
19      if pos >= len(tokens):
20          error("Unexpected end of input in M")
21      lookahead = tokens[pos]
22      if lookahead.startswith('T'):
23          match('T')
24          match("'")
25      elif lookahead.startswith(''):
26          match('')
27      else:
28          error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['T', '*']))
29
30  def parse_input(input_str):
31      global tokens, pos
32      tokens = list(input_str)
33      pos = 0
34      parse_M()
35      print("Input accepted.")
36
37  def main():
38      import sys
39      if len(sys.argv) > 1:
40          input_str = sys.argv[1]
41      else:
42          input_str = sys.stdin.read()
43      parse_input(input_str)
44
45  if name == "main":
46      main()

Failed input examples:
TK

Patch:

@@ -22,7 +22,7 @@ def parse_M():
     if lookahead.startswith('T'):
         match('T')
-        match("'")            
+        match("K")            
     elif lookahead.startswith('*'):
         match('*')
     else:

PLEASE DO NOT ADD MARKDOWN TAG LIKE ```diff``` IN YOUR RESPONSE(***IMPORTANT***).
PLEASE MAKE ONLY MINIMAL CHANGES TO THE CODE.
PLEASE DON'T MODIFY ERROR HANDLING. 
"""

def localise_program_input(program, corrupted_text, backend, model):
    ai = AIInterface(backend, model)
    return ai.get_response(
        repair_prompt,
        "parser code:\n" + program + "\ncorrupted_input:\n" + corrupted_text
    )

def localise_program(program, examples, backend, model):
    ai = AIInterface(backend, model)
    # # Annotate parser code with line numbers for AI reference
    annotated = [f"{i} {line}" for i, line in enumerate(program.splitlines(), start=1)]
    # Prepare few-shot examples of failed inputs (deduplicated)
    examples_block = "\n".join(examples)
    prompt_input = (
        "parser code with line numbers:\n"
        + "\n".join(annotated)
        + "\nThis parser failed in these testcases:\n"
        + examples_block
    )
    # Call the AI interface and clean the returned text while preserving token usage
    # print(prompt_input)
    resp = ai.get_response(program_localisation_prompt, prompt_input)
    text = remove_markdown_tags(remove_think_tags(resp.response_text))
    resp.response_text = text
    return resp
