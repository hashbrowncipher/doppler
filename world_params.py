from numpy import array


SAMPLE_RATE_HERTZ = 48000
CHANNELS = 8
SPEED_OF_SOUND_METERS_SECOND = 340.29

MIC_COORDS = array([
	[0.0, 0.0, 0.0],
	[1.0, 0.0, 0.0],
	[0.0, 1.0, 0.0],
	[0.0, 0.0, 1.0],
	[1.0, 1.0, 0.0],
	[0.0, 1.0, 1.0],
	[1.0, 0.0, 1.0],
	[1.0, 1.0, 1.0],
])
