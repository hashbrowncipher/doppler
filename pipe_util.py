import fileinput


def split_fileinput(type_tuple):
    """Yields tuples with the given types from fileinput."""
    for line in fileinput.input():
        tokens = line.split()
        yield tuple(
            type_const(token)
            for type_const, token
            in zip(type_tuple, tokens)
        )


def join_output(l):
	"""Take a tuple for output and make a string for piping."""
	print ' '.join(str(item) for item in l)
