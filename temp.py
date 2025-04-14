from grammar_gen import gen
parser_code, examples, grammar, nonterminals, terminals = gen(10, 10, 5, 5)
# Print example derivations
print("\nExample input strings:")
for ex in examples:
    print("  " + ex)

# Write the generated parser to a file
with open("generated_parser.py", "w") as f:
    f.write(parser_code)

print("\nParser code has been generated in 'generated_parser.py'.")