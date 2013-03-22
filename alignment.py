from collections import deque

from numpy import array

from pipe_util import split_fileinput
from pipe_util import join_output
from pipe_util import ALIGN_INPUT_FORMAT
from pipe_util import MULTILATERATE_INPUT_FORMAT
from world_params import CHANNEL_COUNT
from world_params import SAMPLE_RATE_HERTZ
from world_params import SPEED_OF_SOUND_METERS_SECOND
from world_params import MAX_MIC_DELAY_SECONDS


def first(l):
	"""Return the first non-None object in l."""
	for i in l:
		if i is not None:
			return i


def detect_missed_event(current_timestep, timestep_queues,
	threshold_timesteps):
	"""If the current time is greater than the maximum delay away from any of
	the currently aligned events, then we've missed an event."""
	for timestep_queues in timestep_queues:
		if (len(timestep_queues) > 0
			and current_timestep - timestep_queues[0] >= threshold_timesteps):
			return True
	return False


def timesteps_to_timestep_distances(timesteps):
	"""Takes a tuple of times (possibly with some Nones) and returns the tuple
	of time, (distances)."""
	key_timestep = first(timesteps)
	distances_meters = [
		float(timestep) / SAMPLE_RATE_HERTZ * SPEED_OF_SOUND_METERS_SECOND if timestep is not None else None
		for timestep
		in timesteps
	]
	return key_timestep, distances_meters


def align(channel__event_timestep_stream, allow_dropped_events=False):
	"""Each microphone should see the same number of peaks arriving in the
	same order (unless the dart is faster than sound!). So have some queues of
	events from every mic, then ouput the times of the same event arriving at
	every mic.

	event_stream must be a generator of (channel int, time float).
	Yields time + 8-tuples of distances.
	"""
	timestep_queues = tuple(deque() for i in range(CHANNEL_COUNT))

	for channel, event_timestep in channel__event_timestep_stream:
		# In on the right.
		timestep_queues[channel].append(event_timestep)

		# Check to see if any peaks could be missing at this point. This
		# should be detectable as an empty channel queue.
		if (allow_dropped_events and
			detect_missed_event(
				event_timestep,
				timestep_queues,
				MAX_MIC_DELAY_TIMESTEPS
			)):
			for timestep_queue in timestep_queues:
				if len(timestep_queue) < 1:
					timestep_queue.append(None)

		# If we've seen a peak on every channel,
		if all(
			len(timestep_queue) > 0
			for timestep_queue
			in timestep_queues
		):
			# yield all those relative times.
			yield timesteps_to_timestep_distances(tuple(
				# Out on the left.
				timestep_queue.popleft()
				for timestep_queue
				in timestep_queues
			))


if __name__ == '__main__':
	for timestep, aligned_distances in align(split_fileinput(ALIGN_INPUT_FORMAT)):
		join_output(MULTILATERATE_INPUT_FORMAT, timestep, *aligned_distances)
