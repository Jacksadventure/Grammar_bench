import random
import string
from ultility import validation_check
MAX_APPTEMPT = 10

def mutate(original,terminals):
    while(MAX_APPTEMPT):
        ## randomly select a position in the string
        pos = random.randint(0, len(original)-1)
        ## randomly select a lowercase character to replace it with
        new_char = random.choice(terminals)
        ## replace the character at position pos with new_char
        new = original[:pos] + new_char + original[pos+1:]
        if not validation_check(new):
            return new
    else:
        print("Could not generate a mutation")
        return ""
    
    