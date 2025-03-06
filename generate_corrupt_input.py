import random
import string
from ultility import validation_check
MAX_APPTEMPT = 10

def mutate(original,terminals):
    while(MAX_APPTEMPT):
        new_char = random.choice(terminals)
        new = original[:-1] + new_char
        if not validation_check(new):
            return new
    else:
        print("Could not generate a mutation")
        return ""
    
    