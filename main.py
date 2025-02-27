from grammar_gen import gen
from generate_corrupt import mutate
from repair import repair
from ultility import levenshtein_distance
MAX_TESTS = 1
MAX_EXAMPLES = 10
def main():
    for i in range(MAX_TESTS):
        print(f"========Test {i+1}========")
        code, examples,terminals = gen(10,10,50,MAX_EXAMPLES)
        print ("Generated code:")
        print(code)
        for index, example in enumerate(examples):
            print(f"========Test {i+1} Original {index}========")
            print(f"mutation: {example}")
            corrupted = mutate(example,terminals)
            if corrupted:
                print(f"corrupted: {corrupted}")
                repaired = repair(code,corrupted,"ollama","phi3:14b")
                print(f"repaired: {repaired}")
                print(levenshtein_distance(example,repaired))
            
if __name__ == "__main__":
    main()