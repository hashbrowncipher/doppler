import fileinput
import struct


def split_fileinput(type_string):
    """Yields tuples with the given types from fileinput."""
    for line in fileinput.input():
		yield struct.unpack(type_string, line)


def join_output(type_string, l):
	"""Take a tuple for output and make a string for piping."""
	print struct.pack(type_string, l)
