# Minimal helper to reflect a patch change where a sequence '`', 'S' is replaced with '`', 'X', 'X'
def adjust_sequence_for_backtick(la_seq):
    # la_seq is a list/iterable of single-character tokens
    out = []
    for la in la_seq:
        if la == '`':
            out.extend(['`','X','X'])
        else:
            out.append(la)
    return out