from numpy import array
from numpy import logical_and
from numpy import logical_xor
from numpy import nonzero
from numpy import signbit

from pipe_util import ALIGN_INPUT_FORMAT
from pipe_util import join_output
from pipe_util import split_fileinput
from pipe_util import ZERO_DETECTION_INPUT_FORMAT
from world_params import CHANNEL_COUNT
from world_params import DART_FREQ_HERTZ
from world_params import SAMPLE_RATE_HERTZ


WAVELENGTH_SAMPLES = SAMPLE_RATE_HERTZ / DART_FREQ_HERTZ


def zero_detection(sample_stream):
	"""Make events for 0-crossings.

	sample_stream must be a generator of CHANNEL_COUNT-tuples of values that
		represent the current microphone level.
	Yields channel ID, time tuples.
	"""
	last_samples_sign = None
	samples_since_zero = array([WAVELENGTH_SAMPLES] * CHANNEL_COUNT)

	for timestep, samples in enumerate(sample_stream):
		samples_sign = signbit(samples)
		if last_samples_sign is not None:
			sign_changes = logical_and(samples_sign, ~last_samples_sign)
			sign_changes = logical_and(sign_changes, samples_since_zero > 2 * WAVELENGTH_SAMPLES / 3)
			for channel in nonzero(sign_changes)[0]:
				yield channel, timestep

			samples_since_zero[sign_changes] = 0
			samples_since_zero[~sign_changes] += 1

		last_samples_sign = samples_sign


if __name__ == '__main__':
	for channel, event_timestep in zero_detection(split_fileinput(ZERO_DETECTION_INPUT_FORMAT)):
		join_output(ALIGN_INPUT_FORMAT, (channel, event_timestep))
