from itertools import combinations
from operator import itemgetter
import sys

from numpy import array
from numpy import random
from numpy import concatenate
from numpy import sum
from numpy import mean
from numpy.linalg.linalg import pinv
from numpy.linalg.linalg import LinAlgError
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cdist
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

from pipe_util import split_fileinput
from pipe_util import join_output
from world_params import CHANNEL_COUNT
from world_params import MIC_COORDS_METERS


FAKE_DART_METERS = array([1.5, 2, 0.5])

MIC_DART_DISTANCES_METERS = array([euclidean(mic, FAKE_DART_METERS) for mic in MIC_COORDS_METERS])


def transpose_1D(M):
	"""numpy is silly and won't let you transpose a N x 1 ndarray to a 1 x N
	ndarray."""
	return M.reshape(len(M), 1)


def multilaterate(mic_positions, time__mic_dart_distances_stream):
	"""Take a stream of mic - dart distances and yield coordinates.

	mic_positions must be a a N x 3 array of coordinates of each mic.
	time__mic_dart_distances_stream must be a generator of time + CHANNEL *
		distances from mic to dart.
	Yields time, 3D coords of dart.
	"""
	mic_positions = array(mic_positions)
	origin = mic_positions[0]
	mic_positions = mic_positions - origin

	for time__mic_dart_distances in time__mic_dart_distances_stream:
		time = time__mic_dart_distances[0]
		mic_dart_distances = array(time__mic_dart_distances[1:])

		# The algorithm fails on any 0 - m distance degeneracies. Add some
		# wiggle if so.
		degeneracies = (mic_dart_distances[1:] == mic_dart_distances[0])
		mic_dart_distances[1:] += 1.0e-12 * degeneracies

		vt = mic_dart_distances - mic_dart_distances[0]
		free_vt = vt[2:]

		A = 2.0 * mic_positions[2:, 0] / free_vt - 2.0 * mic_positions[1, 0] / vt[1]
		B = 2.0 * mic_positions[2:, 1] / free_vt - 2.0 * mic_positions[1, 1] / vt[1]
		C = 2.0 * mic_positions[2:, 2] / free_vt - 2.0 * mic_positions[1, 2] / vt[1]
		D = free_vt - vt[1] - sum(mic_positions[2:, :] ** 2, axis=1) / free_vt + sum(mic_positions[1] ** 2) / vt[1]

		M = concatenate([transpose_1D(A), transpose_1D(B), transpose_1D(C)], axis=1)

		try:
			yield time, pinv(M).dot(-transpose_1D(D)).reshape(3) + origin
		except LinAlgError:
			sys.stderr.write('Could not multilaterate at t = %f\n' % time)


if __name__ == '__main__':
	for time, coordinates in multilaterate(MIC_COORDS_METERS, split_fileinput([float] + [float] * CHANNEL_COUNT)):
		join_output([time] + list(coordinates))
