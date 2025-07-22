"""
This generator (grammar_gen.py) produces a random LL(1) grammar and a
standalone recursive descent parser.

The parser generation now:
- INLINES non-terminals that are only used once.
- OPTIMIZES right-recursive rules (e.g., A -> alpha A | epsilon) into 'while' loops.
- PREVENTS the generation of unsafe, non-terminating self-recursion.
"""

import random
import string
from itertools import product as _itertools_product

# ---------------------------
# Step 1: Generate a Random Grammar (WITH ANTI-RECURSION FIX)
# ---------------------------
def generate_random_grammar(
    num_nonterminals=10,
    num_terminals=None,
    nonterminal_prob=0.5,
    loop_prob=0.3,
    max_productions=5,
    max_rhs_length=5,
):
    """
    Generate a random LL(1) grammar, ensuring it is free of problematic
    self-recursion and non-terminating loops.
    """
    if num_terminals is None: num_terminals = num_nonterminals
    if max_rhs_length < 1: raise ValueError("max_rhs_length must be at least 1.")
    ALPHABET_NT = list(string.ascii_uppercase)
    random.shuffle(ALPHABET_NT)
    def _generate_labels(a, c):
        l, n = [], 1
        while len(l) < c:
            for p in _itertools_product(a, repeat=n):
                l.append(''.join(p));
                if len(l) >= c: break
            n += 1
        return l[:c]
    all_nonterminals = _generate_labels(ALPHABET_NT, num_nonterminals)
    ALPHABET_T = list(string.ascii_letters+string.digits+"'!#$%&'()*+,-./:;<=>?@[]^_`{|}~'")
    random.shuffle(ALPHABET_T)
    if len(ALPHABET_T) < num_terminals: raise ValueError("Not enough unique terminals.")
    terminals = ALPHABET_T[:num_terminals]
    
    grammar = {}
    
    for i, nt in enumerate(all_nonterminals):
        prods, local_available_firsts = [], terminals[:]; random.shuffle(local_available_firsts)
        has_terminating_production, has_forward_link = False, (i + 1 >= len(all_nonterminals))

        # --- SAFE LOOP GENERATION ---
        # This block specifically creates the A -> alpha A | epsilon structure.
        # This is the ONLY place where direct right-recursion is now allowed.
        if random.random() < loop_prob and max_productions >= 2 and local_available_firsts:
            first_term = local_available_firsts.pop()
            # Alpha can contain terminals or *other* future non-terminals.
            possible_alpha_nts = all_nonterminals[i+1:]
            
            alpha = [first_term]
            for _ in range(random.randint(0, max_rhs_length - 2)):
                 alpha.append(random.choice(terminals if not possible_alpha_nts else terminals + possible_alpha_nts))
            
            # The final structure is [alpha..., nt] and an epsilon production [].
            prods.extend([alpha + [nt], []])
            has_terminating_production = True

        # --- REGULAR PRODUCTION GENERATION ---
        num_prods_to_generate = random.randint(1, min(max_productions, len(terminals)))
        for prod_idx in range(num_prods_to_generate):
            if not local_available_firsts: break
            first_term = local_available_firsts.pop(); rhs, is_rhs_terminating = [first_term], True
            must_add_forward_link = (not has_forward_link and prod_idx == num_prods_to_generate - 1)
            rhs_len = random.randint(1, max_rhs_length)

            for _ in range(1, rhs_len):
                # --- MODIFIED LOGIC ---
                # The pool of possible non-terminals for the RHS *excludes* the current NT (nt).
                # This prevents unsafe self-recursion like A -> ... A ...
                # We only allow references to *future* non-terminals.
                possible_rhs_nts = all_nonterminals[i+1:]
                
                if random.random() < nonterminal_prob and possible_rhs_nts:
                    is_rhs_terminating = False
                    nt_choice_pool = possible_rhs_nts
                    if must_add_forward_link:
                        # If we must add the forward link, don't pick it randomly.
                        nt_choice_pool = [n for n in possible_rhs_nts if n != all_nonterminals[i+1]]
                    
                    if nt_choice_pool:
                      rhs.append(random.choice(nt_choice_pool))
                    else:
                      rhs.append(random.choice(terminals))
                else:
                    rhs.append(random.choice(terminals))

            # Inject the mandatory forward link if it hasn't been added yet.
            if must_add_forward_link:
                next_nt = all_nonterminals[i+1]
                insert_pos = random.randint(1, len(rhs))
                rhs.insert(insert_pos, next_nt); has_forward_link, is_rhs_terminating = True, False
            
            prods.append(rhs)
            if is_rhs_terminating: has_terminating_production = True
        
        # Post-checks for reachability and termination.
        if not has_forward_link and local_available_firsts:
            prods.append([local_available_firsts.pop(), all_nonterminals[i+1]])
        if not has_terminating_production and local_available_firsts:
            prods.append([local_available_firsts.pop()])
        
        if prods: grammar[nt] = prods

    # Final decoration for output
    decorated_nonterminals = [f'<{nt}>' for nt in all_nonterminals]; decorated_grammar = {}
    for nt in all_nonterminals:
        if nt not in grammar: continue
        decorated_nt, prods = f'<{nt}>', grammar[nt]; decorated_prods = []
        for prod in prods:
            decorated_prods.append([f'<{s}>' if s in all_nonterminals else s for s in prod])
        decorated_grammar[decorated_nt] = decorated_prods
    return decorated_grammar, decorated_nonterminals, terminals


# ---------------------------
# Step 2: Example Generation (Unchanged)
# ---------------------------
def generate_example_string(grammar, symbol, max_depth=10):
    if symbol not in grammar or max_depth <= 0:
        return "" if (isinstance(symbol, str) and symbol.startswith('<')) else symbol
    prods = sorted(grammar[symbol], key=len); prod = random.choice(prods[:2]); result = []
    for s in prod:
        result.append(generate_example_string(grammar, s, max_depth-1) if s in grammar else s)
    return "".join(result)


# ---------------------------
# Step 3: Parser Code Generation (Unchanged, already handles safe loops)
# ---------------------------
def generate_parser_code(grammar, nonterminals, start_symbol):

    # ---- 1. 去掉装饰 (<...>)，构造裸 CFG ----
    bare_nonterminals = [nt[1:-1] for nt in nonterminals]
    bare_start = start_symbol[1:-1]
    bare_grammar = {}
    is_nullable = {}
    for dec_nt, prods in grammar.items():
        nt = dec_nt[1:-1]
        bare_grammar[nt] = []
        for p in prods:
            if len(p) == 0:
                is_nullable[nt] = True
            else:
                bare_grammar[nt].append([sym[1:-1] if sym.startswith('<') else sym for sym in p])
        if is_nullable.get(nt, False) and nt not in bare_grammar:
            bare_grammar[nt] = []

    grammar = bare_grammar
    nonterminals = bare_nonterminals

    # ---- 2. 计算 FIRST 集 ----
    first_sets = {nt: set() for nt in nonterminals}
    EPSILON = object()
    for nt in nonterminals:
        if is_nullable.get(nt, False):
            first_sets[nt].add(EPSILON)
    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                nullable_prefix = True
                for sym in prod:
                    if sym in nonterminals:
                        before = len(first_sets[nt])
                        first_sets[nt].update(x for x in first_sets[sym] if x is not EPSILON)
                        if len(first_sets[nt]) > before:
                            changed = True
                        if EPSILON not in first_sets[sym]:
                            nullable_prefix = False
                            break
                    else:
                        if sym not in first_sets[nt]:
                            first_sets[nt].add(sym)
                            changed = True
                        nullable_prefix = False
                        break
                if nullable_prefix and EPSILON not in first_sets[nt]:
                    first_sets[nt].add(EPSILON)
                    changed = True

    def get_first_set_of_sequence(sequence):
        """用于普通产生式的前瞻集合"""
        look = set()
        for sym in sequence:
            if sym not in nonterminals:
                look.add(sym)
                return look
            look.update(x for x in first_sets[sym] if x is not EPSILON)
            if EPSILON not in first_sets[sym]:
                return look
        return look  # 全部可空

    def is_iterative_rule(nt):
        """
        判断是否是形如 A -> alpha A | ε 的结构。
        条件：
            1. 有 ε 产生式
            2. 存在产生式 prod 满足 prod[-1] == nt
        返回 (True, alpha) 或 (False, None)
        """
        if not is_nullable.get(nt, False):
            return False, None
        for prod in grammar.get(nt, []):
            if prod and prod[-1] == nt:
                return True, prod[:-1]
        return False, None

    # ---- 3. 代码块生成 ----
    memo = {}
    def generate_code_block_for_nt(nt, indent_level):
        key = (nt, indent_level)
        if key in memo:
            return memo[key]
        indent = '    ' * indent_level
        lines = []

        iterative, base_prod = is_iterative_rule(nt)
        if iterative:
            lookahead_set = get_first_set_of_sequence(base_prod)
            conds = " or ".join([f"tokens[pos] == {repr(t)}" for t in sorted(lookahead_set)])
            if not conds:
                conds = "False"
            lines.append(f"{indent}# Iterative rule for <{nt}>: while {base_prod}")
            lines.append(f"{indent}while pos < len(tokens) and ({conds}):")
            for sym in base_prod:
                lines.extend(generate_code_for_symbol(sym, indent_level + 1))
        else:
            lines.append(f"{indent}# Standard logic for <{nt}>")
            lines.append(f"{indent}if pos >= len(tokens):")
            if is_nullable.get(nt, False):
                lines.append(f"{indent}    pass  # nullable <{nt}> at EOF")
            else:
                lines.append(f"{indent}    raise ParseError('Unexpected EOF parsing <{nt}>')")
            lines.append(f"{indent}else:")
            lines.append(f"{indent}    la = tokens[pos]")
            prods = grammar.get(nt, [])
            first_branch = True
            used_lookaheads = set()
            for prod in prods:
                lookahead_set = get_first_set_of_sequence(prod)
                if not lookahead_set:
                    # 整个序列可空，不在这里处理（交由 nullable 分支）
                    continue
                cond_prefix = "if" if first_branch else "elif"
                conds = " or ".join([f"la == {repr(t)}" for t in sorted(lookahead_set)])
                lines.append(f"{indent}    {cond_prefix} {conds}:")
                for sym in prod:
                    lines.extend(generate_code_for_symbol(sym, indent_level + 2))
                used_lookaheads.update(lookahead_set)
                first_branch = False
            if is_nullable.get(nt, False):
                # ε 分支
                cond_prefix = "if" if first_branch else "elif"
                # lookahead 不在所有已使用集合中的情况 + EOF
                lines.append(f"{indent}    {cond_prefix} True:  # epsilon branch for <{nt}>")
                lines.append(f"{indent}        pass")
            else:
                lines.append(f"{indent}    else:")
                lines.append(f"{indent}        raise ParseError(f\"Unexpected token {{la!r}} parsing <{nt}>\")")

        memo[key] = lines
        return lines

    def generate_code_for_symbol(symbol, indent_level):
        indent = '    ' * indent_level
        if symbol not in nonterminals:
            return [f"{indent}match({repr(symbol)})"]
        else:
            return generate_code_block_for_nt(symbol, indent_level)

    # ---- 4. 组装最终代码 ----
    code_lines = [
        "import sys",
        "tokens = []",
        "pos = 0",
        "class ParseError(Exception): pass",
        "",
        "def match(expected):",
        "    global pos",
        "    if pos < len(tokens) and tokens[pos] == expected:",
        "        pos += 1",
        "    else:",
        "        got = tokens[pos] if pos < len(tokens) else 'EOF'",
        "        raise ParseError(f\"Expected {expected!r}, got {got!r}\")",
        "",
        "def parse(input_str):",
        "    global tokens, pos",
        "    tokens = list(input_str.strip())",
        "    pos = 0",
    ]
    # start symbol 展开
    code_lines.extend(generate_code_block_for_nt(bare_start, 1))
    code_lines.extend([
        "    if pos < len(tokens):",
        "        raise ParseError(f\"Extra characters at end: {''.join(tokens[pos:])}\")",
        "    print('Input accepted.')",
        "",
        "if __name__ == '__main__':",
        "    if len(sys.argv) > 1:",
        "        try:",
        "            parse(sys.argv[1])",
        "        except ParseError as e:",
        "            print('Input rejected.')",
        "            print(e)",
        "    else:",
        "        print('Usage: python generated_parser.py <string_to_parse>')",
    ])
    return '\n'.join(code_lines)

# ---------------------------
# Step 4: Main Wrapper (Unchanged)
# ---------------------------
def gen(
    numnonterminals, max_original_examples, nonterminal_prob,
    loop_prob=0.3, numterminals=None, max_rhs_length=3, maxproductions=3,
):
    grammar, nonterminals, terminals = generate_random_grammar(
        num_nonterminals=numnonterminals, nonterminal_prob=nonterminal_prob,
        loop_prob=loop_prob, max_productions=maxproductions, max_rhs_length=max_rhs_length,
    )
    if not nonterminals:
        print("Warning: Grammar generation resulted in no nonterminals.")
        return None, set(), {}, [], []
    start_symbol = nonterminals[0]
    examples = set()
    for _ in range(max_original_examples * 5):
        ex = generate_example_string(grammar, start_symbol)
        if 3 <= len(ex) < 15 and ex not in examples:
            examples.add(ex)
            if len(examples) >= max_original_examples: break
    parser_code = generate_parser_code(grammar, nonterminals, start_symbol)
    return parser_code, examples, grammar, nonterminals, terminals

if __name__ == '__main__':
    code, exs, g, nts, ts = gen(
        numnonterminals=8, max_original_examples=3, nonterminal_prob=0.4,
        loop_prob=0.3, max_rhs_length=4, maxproductions=3,
    )
    if code:
        print("--- Generated Grammar ---")
        for nt in nts:
            prods = g.get(nt, []); prod_strs = [' '.join(p) if p else 'ε' for p in prods]
            print(f"{nt.ljust(5)} -> {' | '.join(prod_strs)}")
        print("\n--- Example Derivations ---")
        print(exs if exs else "No suitable examples were generated.")
        with open("generated_parser.py", "w") as f: f.write(code)
        print("\nParser code saved to generated_parser.py")