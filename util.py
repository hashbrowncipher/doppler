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

def sine(freq, offset=0):
    return [math.sin(offset + i * 2 * math.pi * freq / SAMPLE_RATE_HERTZ)
            for i in range(BUFFER_SIZE)]

def add_signals(s1, s2, r=1):
    return [s1[i] + r * s2[i] for i in range(len(s1))]

def add_noise(signal, noise_ratio=0.4):
    noise = [0] * len(signal)

    # adding a bunch of sines with random frequency and amplitude
    for _ in range(500):
        moar_noise = sine(random.randint(1,24000), 2 * math.pi * random.random())
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

def index_from_freq(freq):
    return int(freq * BUFFER_SIZE / SAMPLE_RATE_HERTZ)

def fft(signal):
    return scipy.fft(signal).tolist()

def spectrum(signal):
    return [x * numpy.conj(x) for x in fft(signal)]


########################################
# filters
########################################

def prepare_multi_band_filter(freq_ranges, size=BUFFER_SIZE):
    mask = [0] * size
    for (low, high) in freq_ranges:
        low = index_from_freq(low)
        high = index_from_freq(high)
        mask = mask[:low] + [1] * (high - low) + mask[high:]
    return mask

def violent_multi_band_pass(signal, mask):
    """ A filter that lets you define a bunch of bands:
    everything outside of these frequency ranges gets mercylessly filtered"""
    assert(len(signal) == len(mask))
    f = fft(signal)
    filtered = [mask[i] * f[i] for i in range(len(signal))]
    return scipy.ifft(filtered).real.tolist()

def violent_band_pass(signal, low_freq, high_freq):
    low = index_from_freq(low_freq)
    high = index_from_freq(high_freq)
    return violent_multi_band_pass(signal,
            [0] * low + [1] * (high - low) + [0] * (BUFFER_SIZE - high)
        )


########################################
# harmonics
########################################

def harmonic_series(freq, n):
    return [freq * i for i in range(1, n+1)]

def ranges_from_series(freqs, precision):
   # factor = 1 + precision
   # return [(f / factor, f * factor) for f in freqs]
    tolerance = freqs[0] * precision
    return [(f - tolerance, f + tolerance) for f in freqs]



########################################
# dart finding
########################################

def find_peak_in(signal, low_freq, high_freq):
    low = index_from_freq(low_freq)
    high = index_from_freq(high_freq)
    maxp = 0
    ind = 0
    for i, p in enumerate(spectrum(signal)[low:high]):
        if p > maxp:
            maxp = p
            ind = i
    return freq_from_index(low + ind)

def make_mask_for_signal(signal, low_freq, high_freq, precision=0.05):
    base = find_peak_in(signal, low_freq, high_freq)
    ranges = ranges_from_series(
            harmonic_series(base, 10),
            precision
        )
    return prepare_multi_band_filter(ranges)


########################################
# test data
########################################

def make_signal(freq, harmonic_pattern):
    signal = [0] * BUFFER_SIZE
    for i, ratio in enumerate(harmonic_pattern):
        signal = add_signals(signal, sine((i + 1) * freq), ratio)
    return signal

harmonic_pattern = [(10 - i) / 10. for i in range(10)]
signal = make_signal(1900, harmonic_pattern)

noisy = add_noise(signal)

def plot(signal, sig_graph, fft_graph):
    sig_graph.plot(signal[:BUFFER_SIZE/4])
    fft_graph.plot(spectrum(signal)[:BUFFER_SIZE/2])

def draw_all():
    fig = plt.figure()
    grid = 420
    sig_graph = fig.add_subplot(grid + 1)
    fft_graph = fig.add_subplot(grid + 2)
    noisy_graph = fig.add_subplot(grid + 3)
    noisyfft_graph = fig.add_subplot(grid + 4)
    filtered_graph = fig.add_subplot(grid + 5)
    filteredfft_graph = fig.add_subplot(grid + 6)
    multifiltered_graph = fig.add_subplot(grid + 7)
    multifilteredfft_graph = fig.add_subplot(grid + 8)
    noisy = add_noise(signal, 0.5)
    filtered = violent_multi_band_pass(noisy, prepare_multi_band_filter([(1500, 2500)]))
    mask = make_mask_for_signal(noisy, 1500, 3000, 0.05)
    multifiltered = violent_multi_band_pass(noisy, mask)
    plot(signal, sig_graph, fft_graph)
    plot(noisy, noisy_graph, noisyfft_graph)
    plot(filtered, filtered_graph, filteredfft_graph)
    plot(multifiltered, multifiltered_graph, multifilteredfft_graph)
    plt.show()


# f = scipy.fft(noisy)[:BUFFER_SIZE/2]

# plt.plot(noisy)
# plt.show()
# plt.plot(f)
# plt.show()

# max_index, max_value = max(enumerate(f), key=lambda x:x[1]
#         if freq_from_index(x[0])>200 else 0)


# print "Freq:", freq_from_index(max_index)


if __name__ == '__main__':
    for timestep, value in enumerate(sine(DART_FREQ_HERTZ)):
        join_output([value] * CHANNELS)
