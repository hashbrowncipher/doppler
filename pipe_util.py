import fileinput
import struct


def split_fileinput(fmt):
    """Yields tuples with the given types from fileinput."""
    for line in fileinput.input():
		yield struct.unpack(fmt, line[:-1])


def join_output(fmt, *l):
	"""Take a tuple for output and make a string for piping."""
	print struct.pack(fmt, *l)
