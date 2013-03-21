from math import cos, pi

speed_of_sound = 343 # meters/second
sample_frequency = 48000 # samples/second
# stop tracking emitted sounds after window_length seconds
window_length = 0.001

sample_length = 1.0 / sample_frequency
samples_by_distance = sample_frequency / speed_of_sound # samples/meter
bucket_count = int(sample_frequency * window_length)

tau = 2 * pi

def distance(a, b):
    return sum(map(lambda (x, y): (x - y)**2, zip(a, b)))**0.5 

def simple_cos(f):
    frequency = f * sample_length * tau
    return lambda s: cos(frequency * s)

class NerfSimulator(object):
    mics = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)]
    mic_count = len(mics)

    def blank_bucket(self):
        return [0]*len(self.mics)

    def __init__(self):
        self.buckets = [self.blank_bucket() for i in xrange(bucket_count)]
        self.window_start = 0

    def emit(self, position, pressure):
        for i in xrange(self.mic_count):
            target_bucket = int(distance(position, self.mics[i]) * samples_by_distance)
            print target_bucket
            if target_bucket < bucket_count:
                actual_bucket = (self.window_start + target_bucket) % bucket_count
                self.buckets[actual_bucket][i] += pressure
        print self.buckets

    def finalize_bucket(self):
        # after a certain time it will be impossible for the dart to further influence the bucket
        # (the sound can't travel back in time, after all)
        ret = self.buckets[self.window_start]
        self.buckets[self.window_start]=self.blank_bucket()
        self.window_start = (self.window_start + 1) % bucket_count
        return ret

    def throw_dart(self, position_0, velocity, samples, signal):
        position = position_0
        for i in xrange(samples):
            pressure = signal(i)
            self.emit(position, signal(i))
            yield self.finalize_bucket()
            displacement = [i*sample_length for i in velocity]
            position = map(sum, zip(position, displacement))
