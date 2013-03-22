CHANNELS = 8

def align(events):
	"""Assume that every microphone will see every peak. Then each microphone
	will see the same number of peaks arriving in the same order (unless the
	dart is faster than sound). So have some queues of events from every mic,
	then ouput the times of the same event arriving at every mic.

	events must be a generator of (channel int, time float).
	"""
	queues = tuple([[]] * CHANNELS)

	for channel, event_t in events:
		queues[channel].push(event_t)

		# If we've seen a peak on every channel,
		if all(len(queue) > 0 for queue in queues):
			# yield all those relative times.
			yield tuple(queue.pop(0) for queue in queues)
