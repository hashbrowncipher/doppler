from numpy import signbit
from numpy import logical_xor

from pipe_util import split_fileinput
from pipe_util import join_output
from world_params import CHANNEL_COUNT
from world_params import SAMPLE_RATE_HERTZ


def zero_detection(sample_stream):
	"""Make events for 0-crossings.

	sample_stream must be a generator of CHANNEL_COUNT-tuples of values that
		represent the current microphone level.
	Yields channel ID, time tuples.
	"""
	last_samples_sign = None
	for timestep, samples in enumerate(sample_stream):
		samples_sign = signbit(samples)
		if last_samples_sign is not None:
			sign_changes = logical_xor(last_samples_sign, samples_sign)
			for channel, sign_change in enumerate(sign_changes):
				if sign_change:
					yield channel, float(timestep) / float(SAMPLE_RATE_HERTZ)
		last_samples_sign = samples_sign


if __name__ == '__main__':
	for channel_event_t in zero_detection(split_fileinput([float] * CHANNEL_COUNT)):
		join_output(channel_event_t)
