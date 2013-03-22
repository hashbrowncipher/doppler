from itertools import combinations
from operator import itemgetter

from numpy import array
from numpy import random
from numpy import concatenate
from numpy import sum
from numpy import mean
from numpy.linalg import solve
from numpy.linalg.linalg import pinv
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cdist
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform


mics = array([
	[1.0, 0.0, 0.0],
	[0.0, 3.0, 0.0],
	[0.0, 0.0, 2.0],
	[1.0, 1.0, 1.0],
	[4.0, 2.0, 4.0],
	[0.0, 0.0, 9.0],
	[5.0, 2.0, -2.0],
])
fake_dart = array([1.5, 2, 0.5])

mic_mic_distances = squareform(pdist(mics, 'euclidean'))
mic_dart_distances = array([euclidean(mic, fake_dart) for mic in mics])
mic_dart_distances += random.normal(0.0, 0.1, mic_dart_distances.shape)


def transpose_1D(M):
	"""numpy is silly and won't let you transpose a N x 1 ndarray to a 1 x N
	ndarray."""
	return M.reshape(len(M), 1)


def multilaterate(mic_positions, mic_dart_distances_stream):
	"""Take a stream of mic - dart distances and yield coordinates.

	mic_positions must be a a N x 3 array of coordinates of each mic.
	mic_dart_distances must be a generator of 1 x N array of arbitrary offset
		distances from dart to each mic.
	"""
	mic_positions = array(mic_positions)
	origin = mic_positions[0]
	mic_positions -= origin

	for mic_dart_distances in mic_dart_distances_stream:
		mic_dart_distances = array(mic_dart_distances)

		vt = mic_dart_distances[2:] - mic_dart_distances[0]

		A = 2.0 * mic_positions[2:, 0] / vt - 2.0 * mic_positions[1, 0] / vt[1]
		B = 2.0 * mic_positions[2:, 1] / vt - 2.0 * mic_positions[1, 1] / vt[1]
		C = 2.0 * mic_positions[2:, 2] / vt - 2.0 * mic_positions[1, 2] / vt[1]
		D = vt - vt[1] - sum(mic_positions[2:, :] ** 2, axis=1) / vt + sum(mic_positions[1] ** 2) / vt[1]

		M = concatenate([transpose_1D(A), transpose_1D(B), transpose_1D(C)], axis=1)

		yield pinv(M).dot(-transpose_1D(D)).reshape(3) + origin
