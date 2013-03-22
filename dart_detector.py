import sys
import filtering_utils
import fileinput
import struct
import pipe_util


BUFFER_SIZE = 2048

LOW_FREQ = 1900
HIGH_FREQ = 2800

N_MIC = 2
# buffers initially 0

windows = [[0] * BUFFER_SIZE] * N_MIC

def filter_dart(line):
    # The input is 8 channels of 2-byte (unsigned short) signals.
    unpacked_samples = line

    # drop oldest sample
    for w in windows:
        w = w[1:]

    # append newest sample
    for i, sample in enumerate(unpacked_samples):
        windows[i].append(sample)


    return filtering_utils.is_there_a_dart(windows[0], LOW_FREQ, HIGH_FREQ)

if __name__ == '__main__':
    try:
        for line in pipe_util.split_fileinput('HH'):
            print filter_dart(line)
    except KeyboardInterrupt:
        pass
