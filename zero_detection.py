from numpy import array
from numpy import logical_and
from numpy import logical_xor
from numpy import nonzero
from numpy import signbit

from pipe_util import split_fileinput
from pipe_util import join_output
from world_params import CHANNELS
from world_params import DART_FREQ_HERTZ
from world_params import SAMPLE_RATE_HERTZ


WAVELENGTH_SAMPLES = SAMPLE_RATE_HERTZ / DART_FREQ_HERTZ


def zero_detection(sample_stream):
	"""Make events for 0-crossings.

	sample_stream must be a generator of CHANNELS-tuples of values that
		represent the current microphone level.
	Yields channel ID, time tuples.
	"""
	last_samples_sign = None
	samples_since_zero = array([WAVELENGTH_SAMPLES]*CHANNELS)

	for timestep, samples in enumerate(sample_stream):
		samples_sign = signbit(samples)
		if last_samples_sign is not None:
			sign_changes = logical_and(samples_sign, ~last_samples_sign)
			sign_changes = logical_and(sign_changes, samples_since_zero > 2 * WAVELENGTH_SAMPLES / 3)
			for channel in nonzero(sign_changes)[0]:
				yield channel, float(timestep) / float(SAMPLE_RATE_HERTZ)
	
			samples_since_zero[sign_changes] = 0
			samples_since_zero[~sign_changes] += 1

		last_samples_sign = samples_sign


if __name__ == '__main__':
	for channel_event_t in zero_detection(split_fileinput([float] * CHANNELS)):
		join_output(channel_event_t)
