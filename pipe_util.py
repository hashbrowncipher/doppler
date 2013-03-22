"""Uses struct for more efficient data streaming between parts.
http://docs.python.org/2/library/struct.html#format-characters
has information on the type_strings being used.
"""
import fileinput
import struct

from world_params import CHANNEL_COUNT


# Input is a double per channel
ZERO_DETECTION_INPUT_FORMAT = 'd' * CHANNEL_COUNT
# Channel id is a short, double time in seconds
ALIGN_INPUT_FORMAT = 'H' + 'd'
# Input one double time in seconds and one double distance per channel
MULTILATERATE_INPUT_FORMAT = 'd' + 'd' * CHANNEL_COUNT
# Display is t, x, y, z all doubles
DISPLAY_INPUT_FORMAT = 'dddd'


# Set True to use struct and pass messages more efficiently; False
# uses strings separated by spaces instead.
USE_BINARY_PACKING = False

# Extend this with more types if we need them, for now unsigned shorts
# and doubles are all we're using.
fmt_chars_to_types = {
    'd': float,
    'H': int,
    'L': long,
}


def split_fileinput(fmt):
    """Yields tuples with the given types from fileinput."""
    if USE_BINARY_PACKING:
        for line in fileinput.input():
            yield struct.unpack(fmt, line)
    else:
        types = [fmt_chars_to_types[fmt_char] for fmt_char in fmt]
        for line in fileinput.input():
            yield list(in_type(x) for in_type, x in zip(types, line.split()))


def join_output(fmt, l):
    """Take a tuple for output and make a string for piping."""
    if USE_BINARY_PACKING:
        print struct.pack(fmt, *l)
    else:
        print ' '.join(str(item) for item in l)
