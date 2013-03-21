import fileinput
import numpy
import struct

#TODO
SAMPLE_TIME = 1
MIN_FREQ = 1
MAX_FREQ = 1

def filter_signal():
	# 8 rolling windows of samples
	windows = [[], [], [], [], [], [], [], []]
	sample_len = 0

	for samples in fileinput.input(mode='rb'):
		# The input is 8 channels of 2-byte (unsigned short) signals.
		unpacked_samples = list(struct.unpack('HHHHHHHH', samples))

		# The dart detector will emit 0s if it doesn't think there's a dart
		# and the entire signal if it does.

		if not all(x == 0 for x in unpacked_samples):
			# If it's not 0s, build up our sample
			sample_len += 1
			for i, sample in enumerate(unpacked_samples):
				windows[i].append(sample)
			continue
		elif sample_len == 0:
			# If it is, but we have nothing stored, wait for data to come in
			continue

		# We recorded some data, and then we stopped - filter and return
		filtered_windows = []
		for mic_window in windows:
			time_arr = numpy.array(mic_window)
			transformed = numpy.fft.fft(time_arr).real
			freqs = numpy.fft.fftfreq(len(time_arr), d=SAMPLE_TIME)

			for i, freq in enumerate(freqs):
				# bandpass
				if freq < MIN_FREQ or freq > MAX_FREQ:
					transformed[i] = 0

			filtered_windows.append(numpy.fft.ifft(transformed))

		for i in range(sample_len):
			packed_filtered_sample = struct.pack('HHHHHHHH', (window[i] for window in filtered_windows))
			print packed_filtered_sample

		windows = [[], [], [], [], [], [], [], []]
		sample_len = 0



if __name__ == '__main__':
	filter_signal()
