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

input_buffers = [[]] * N_MIC
output_buffers = [[]] * N_MIC


def fresh_buffers(full_buffers):
    for i, buf in enumerate(input_buffers):
        input_buffers[i] = buf[BUFFER_SIZE/2:]

def filter_dart(line):

    # append newest sample
    for i, sample in enumerate(line):
        input_buffers[i].append(sample)

    if len(input_buffers[0]) == BUFFER_SIZE:
        for i in range(N_MIC):
            output_buffers[i] = filtering_utils.process(
                    input_buffers[i], LOW_FREQ, HIGH_FREQ)
            fresh_buffers(input_buffers)

    if output_buffers[0]:
        output = [buf[len(input_buffers[0]) - (BUFFER_SIZE/4)]
                for buf in output_buffers]
        pipe_util.join_output("dd", output)

if __name__ == '__main__':
    try:
        for line in pipe_util.split_fileinput('HH'):
            filter_dart(line)
    except KeyboardInterrupt:
        pass
