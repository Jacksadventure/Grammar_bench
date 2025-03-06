import argparse
from grammar_gen import gen
from generate_corrupt_input import mutate
from repair import repair
from ultility import levenshtein_distance,validation_check
from localisation import localise
from patch import replace_function_ast_in_file
from grammar_gen import generate_parser_code
from mutation import mutate_grammar
from file_diff import diff
MAX_TESTS = 1
MAX_EXAMPLES = 100

def program_input_reapir(backend,model):
    SUCCESS = 0
    TOTAL = 0
    for i in range(MAX_TESTS):
        print(f"========Test {i+1}========")
        code, examples,grammar,nonterminals,terminals = gen(5,5,50,MAX_EXAMPLES)
        print ("Generated code:")
        print(code)
        ##  write code to file 
        with open("generated_parser.py","w") as f:
            f.write(code)
        for index, example in enumerate(examples):
            TOTAL += 1  
            print(f"========Test {i+1} Original {index}========")
            print(f"original: {example}")
            corrupted = mutate(example,terminals)
            if corrupted:
                print(f"corrupted: {corrupted}")
                repaired = repair(code,corrupted,backend=backend,model=model)
                print(f"repaired: {repaired}")
                if validation_check(repaired):
                    SUCCESS += 1
                    print("Validation check passed")
                else:
                    print("Validation check failed")
                print(f"levenshtein_distance: {levenshtein_distance(example,repaired)}")
    print(f"Success rate: {SUCCESS/TOTAL*100}%")

def program_reapir(backend,model):
    SUCCESS = 0
    TOTAL = 0
    for i in range(MAX_TESTS):
        print(f"========Test {i+1}========")
        code, _ , grammar ,nonterminals, terminals = gen(5,5,50,MAX_EXAMPLES)
        print ("Generated code:")
        print(code)
        ##  write code to file 
        with open("original_generated_parser.py","w") as f:
            f.write(code)
        ## get corruption code
        corrupted_grammar,new_nonterminals,new_terminals = mutate_grammar(grammar,nonterminals,terminals)
        code = generate_parser_code(corrupted_grammar,new_nonterminals,new_nonterminals[0])
        print ("Corrupted code:")
        print(code)
        ##  write code to file
        with open("corrupted_generated_parser.py","w") as f:
            f.write(code)
        ## get diff
        diff("original_generated_parser.py","corrupted_generated_parser.py")
        # for index, example in enumerate(examples):
        #     TOTAL += 1  
        #     print(f"========Test {i+1} Original {index}========")
        #     print(f"original: {example}")
        #     corrupted = mutate(example,terminals)
        #     if corrupted:
        #         print(f"corrupted: {corrupted}")
        #         print(localise(code,corrupted,backend=backend,model=model))
        #         repaired = repair(code,corrupted,backend=backend,model=model)

def main():
    parser = argparse.ArgumentParser(description='Sample Parser')
    parser.add_argument('--mode', type=str, default='input_repair', help='mode: input_repair or program_repair')
    parser.add_argument('--backend', type=str, default='openai', help='backend: openai / ollama / Claude')
    parser.add_argument('--model', type=str, default='o1-mini-2024-09-12', help='model: model name')
    args = parser.parse_args()
    if args.mode == 'input_repair':
        program_input_reapir(args.backend,args.model)
    elif args.mode == 'program_repair':
        program_reapir(args.backend,args.model)
    else:
        print("Invalid mode")
            
if __name__ == "__main__":
    main()