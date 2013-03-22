import numpy
import scipy
import math
import matplotlib.pyplot as plt
import random

from pipe_util import join_output
from world_params import CHANNELS
from world_params import SAMPLE_RATE_HERTZ
from world_params import DART_FREQ_HERTZ


BUFFER_SIZE = 512

def sine(freq, length):
    for i in range(length):
        yield math.sin(i * 2 * math.pi * freq / SAMPLE_RATE_HERTZ)

def add_signals(s1, s2, r=1):
    return [s1[i] + r * s2[i] for i in range(len(s1))]

def add_noise(signal, noise_ratio=0.2):
    noise = [0] * len(signal)

    # adding a bunch of sines with random frequency and amplitude
    for _ in range(500):
        moar_noise = sine(random.randint(1,24000))
        noise = add_signals(noise, moar_noise, random.random())

    # adding some white noise too
    white_noise = [random.random() for _ in range(len(signal))]
    noise = add_signals(noise, white_noise, 0.5)

    noisy = add_signals(signal, noise, noise_ratio)
    return noisy

def freq_from_index(index):
    """ returns the frequency associated to the index in the fft"""
    return index * SAMPLE_RATE_HERTZ / BUFFER_SIZE


# signal = sine(freq)
# noisy = add_noise(signal)

# f = scipy.fft(noisy)[:BUFFER_SIZE/2]

# plt.plot(noisy)
# plt.show()
# plt.plot(f)
# plt.show()

# max_index, max_value = max(enumerate(f), key=lambda x:x[1]
#         if freq_from_index(x[0])>200 else 0)


# print "Freq:", freq_from_index(max_index)


if __name__ == '__main__':
    for timestep, value in enumerate(sine(DART_FREQ_HERTZ, 10000)):
        join_output([value] * CHANNELS)
