"""Uses struct for more efficient data streaming between parts.
http://docs.python.org/2/library/struct.html#format-characters
has information on the type_strings being used.
"""
import fileinput
import struct

# Set True to use struct and pass messages more efficiently; False
# uses strings separated by spaces instead.
USE_BINARY_PACKING = False

# Extend this with more types if we need them, for now unsigned shorts
# and doubles are all we're using.
fmt_chars_to_types = {
    'd': float,
    'H': int,
}


def split_fileinput(type_string):
    """Yields tuples with the given types from fileinput."""
    if USE_BINARY_PACKING:
        for line in fileinput.input():
            yield struct.unpack(type_string, line)
    else:
        types = [fmt_chars_to_types[fmt_char] for fmt_char in type_string]
        for line in fileinput.input():
            yield (in_type(x) for in_type, x in zip(types, line.split()))


def join_output(type_string, l):
    """Take a tuple for output and make a string for piping."""
    if USE_BINARY_PACKING:
        print struct.pack(type_string, *l)
    else:
        print ' '.join(str(item) for item in l)
