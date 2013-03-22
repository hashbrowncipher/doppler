import numpy
import scipy
import math
import matplotlib.pyplot as plt
import random

BUFFER_SIZE = 512
SAMPLE_RATE = 48000

freq = 2000

def sine(freq, offset=0):
    return [math.sin(offset + i * 2 * math.pi * freq / SAMPLE_RATE)
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
    return index * SAMPLE_RATE / BUFFER_SIZE

def index_from_freq(freq):
    return int(freq * BUFFER_SIZE / SAMPLE_RATE)

def fft(signal):
    return scipy.fft(signal).real.tolist()

def violent_band_pass(signal, f1, f2):
    i1 = index_from_freq(f1)
    i2 = index_from_freq(f2)

    f = fft(signal)
    filtered = ([0] * i1) + f[i1:i2] + ([0] * (BUFFER_SIZE - i2))
    return scipy.ifft(filtered).real.tolist()

def draw_signal(signal):
    fig = plt.figure()
    sig_graph = fig.add_subplot(211)
    fft_graph = fig.add_subplot(212)
    sig_graph.plot(signal)
    fft_graph.plot(fft(signal))
    plt.show()

signal = sine(freq)

noisy = add_noise(signal)

def plot(signal, sig_graph, fft_graph):
    sig_graph.plot(signal)
    fft_graph.plot(fft(signal))

def draw_all():
    fig = plt.figure()
    sig_graph = fig.add_subplot(321)
    fft_graph = fig.add_subplot(322)
    noisy_graph = fig.add_subplot(323)
    noisyfft_graph = fig.add_subplot(324)
    filtered_graph = fig.add_subplot(325)
    filteredfft_graph = fig.add_subplot(326)
    signal = sine(2000)
    noisy = add_noise(signal)
    filtered = violent_band_pass(noisy, 1500, 2500)
    plot(signal, sig_graph, fft_graph)
    plot(noisy, noisy_graph, noisyfft_graph)
    plot(filtered, filtered_graph, filteredfft_graph)
    plt.show()


max_index, max_value = max(enumerate(fft(noisy)), key=lambda x:x[1]
        if freq_from_index(x[0])>200 else 0)


print "Freq:", freq_from_index(max_index)
