from collections import deque

from numpy import array

from pipe_util import split_fileinput
from pipe_util import join_output
from world_params import CHANNELS
from world_params import SPEED_OF_SOUND_METERS_SECOND


def align(event_stream):
	"""Assume that every microphone will see every peak. Then each microphone
	will see the same number of peaks arriving in the same order (unless the
	dart is faster than sound). So have some queues of events from every mic,
	then ouput the times of the same event arriving at every mic.

	event_stream must be a generator of (channel int, time float).
	Yields time + 8-tuples of distances.
	"""
	queues = tuple(deque() for i in range(CHANNELS))

	for channel, event_t in event_stream:
		# In on the right.
		queues[channel].append(event_t)

		# If we've seen a peak on every channel,
		if all(len(queue) > 0 for queue in queues):
			# yield all those relative times.
			# Out on the left.
			yield tuple(queue.popleft() for queue in queues)


if __name__ == '__main__':
	# Channel id is a short, time is a double
	for aligned_times in align(split_fileinput('Hd')):
		aligned_distances = array(aligned_times) * SPEED_OF_SOUND_METERS_SECOND
		# One double for time, plus one double per channel
		join_output('d' * (CHANNELS + 1), [aligned_times[0]] + list(aligned_distances))
