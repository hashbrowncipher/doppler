from numpy import array
from scipy.spatial.distance import pdist


SAMPLE_RATE_HERTZ = 48000
CHANNELS = 8
SPEED_OF_SOUND_METERS_SECOND = 340.29
DART_FREQ_HERTZ = 2000.0

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

# Figure out a threshold for the maximum difference in delays we should
# observe.
MIC_MIC_DISTANCES = pdist(MIC_COORDS, 'euclidean')
DELAY_FUDGE_FACTOR = 1.1
MAX_MIC_DELAY_SECONDS = max(MIC_MIC_DISTANCES) / SPEED_OF_SOUND_METERS_SECOND * DELAY_FUDGE_FACTOR
