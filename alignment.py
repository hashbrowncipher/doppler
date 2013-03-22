from collections import deque

from numpy import array

from pipe_util import split_fileinput
from pipe_util import join_output
from pipe_util import unpack_fileinput
from pipe_util import pack_output
from world_params import CHANNEL_COUNT
from world_params import SPEED_OF_SOUND_METERS_SECOND
from world_params import MAX_MIC_DELAY_SECONDS
from multilateration import MULTILATERATE_INPUT_FORMAT


def first(l):
	"""Return the first non-None object in l."""
	for i in l:
		if i is not None:
			return i


def detect_missed_event(current_time_seconds, time_seconds_queues,
	threshold_seconds):
	"""If the current time is greater than the maximum delay away from any of
	the currently aligned events, then we've missed an event."""
	for time_seconds_queue in time_seconds_queues:
		if (len(time_seconds_queue) > 0
			and current_time_seconds - time_seconds_queue[0] >= threshold_seconds):
			return True
	return False


def times_to_time_distances(times_seconds):
	"""Takes a tuple of times (possibly with some Nones) and returns the tuple
	of time, (distances)."""
	key_time_seconds = first(times_seconds)
	distances_meters = [
		time_seconds * SPEED_OF_SOUND_METERS_SECOND if time_seconds is not None else None
		for time_seconds
		in times_seconds
	]
	return key_time_seconds, distances_meters


ALIGN_INPUT_FORMAT = 'h' + 'f' * CHANNEL_COUNT
def align(channel__event_time_seconds_stream, allow_dropped_events=True):
	"""Each microphone should see the same number of peaks arriving in the
	same order (unless the dart is faster than sound!). So have some queues of
	events from every mic, then ouput the times of the same event arriving at
	every mic.

	event_stream must be a generator of (channel int, time float).
	Yields time + 8-tuples of distances.
	"""
	time_seconds_queues = tuple(deque() for i in range(CHANNEL_COUNT))

	for channel, event_time_seconds in channel__event_time_seconds_stream:
		# In on the right.
		time_seconds_queues[channel].append(event_time_seconds)

		# Check to see if any peaks could be missing at this point. This
		# should be detectable as an empty channel queue.
		if (allow_dropped_events and
			detect_missed_event(
				event_time_seconds,
				time_seconds_queues,
				MAX_MIC_DELAY_SECONDS
			)):
			for time_seconds_queue in time_seconds_queues:
				if len(time_seconds_queue) < 1:
					time_seconds_queue.append(None)

		# If we've seen a peak on every channel,
		if all(
			len(time_seconds_queue) > 0
			for time_seconds_queue
			in time_seconds_queues
		):
			# yield all those relative times.
			yield times_to_time_distances(tuple(
				# Out on the left.
				time_seconds_queue.popleft()
				for time_seconds_queue
				in time_seconds_queues
			))


if __name__ == '__main__':
	for time_seconds, aligned_distances_meters in align(split_fileinput((int, float))):
		pack_output(MULTILATERATE_INPUT_FORMAT, time_seconds, *aligned_distances_meters)
