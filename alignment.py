from collections import deque

CHANNELS = 8

def align(events):
	"""Assume that every microphone will see every peak. Then each microphone
	will see the same number of peaks arriving in the same order (unless the
	dart is faster than sound). So have some queues of events from every mic,
	then ouput the times of the same event arriving at every mic.

	Events must be a generator of (channel int, time float).
	Yields 8-tuples of time floats.
	"""
	queues = tuple(deque() for i in range(CHANNELS))

	for channel, event_t in events:
		# In on the right.
		queues[channel].append(event_t)

		# If we've seen a peak on every channel,
		if all(len(queue) > 0 for queue in queues):
			# yield all those relative times.
			# Out on the left.
			yield tuple(queue.popleft() for queue in queues)
