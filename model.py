from math import cos, pi

speed_of_sound = 343 # meters/second
sample_frequency = 48000 # samples/second
# stop tracking emitted sounds after window_length seconds
window_length = 0.5

sample_length = 1.0 / sample_frequency
samples_by_distance = sample_frequency / speed_of_sound # samples/meter
bucket_count = int(sample_frequency * window_length)

tau = 2 * pi

def distancesq(a, b):
    return sum(map(lambda (x, y): (x - y)**2, zip(a, b)))**0.5 

def simple_cos(f):
    frequency = f * sample_length * tau
    return lambda s: cos(frequency * s)

class NerfSimulator(object):
    mics = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0)]
    mic_count = len(mics)

    def blank_bucket(self):
        return [0]*len(self.mics)

    def __init__(self, position, velocity, signal):
        self.buckets = [self.blank_bucket() for i in xrange(bucket_count)]
        self.time = 0

        self.position = position
        self.velocity = velocity
        self.signal = signal

    def emit(self, position, pressure):
        for i in xrange(self.mic_count):
            d2 = distancesq(position, self.mics[i])
            target_bucket = int(d2**0.5 * samples_by_distance)
            if target_bucket < bucket_count:
                actual_bucket = (self.time + target_bucket) % bucket_count
                self.buckets[actual_bucket][i] += pressure / d2

    def finalize_bucket(self):
        # after a certain time it will be impossible for the dart to further influence the bucket
        # (the sound can't travel back in time, after all)
        window_start = self.time % bucket_count
        ret = self.buckets[window_start]
        self.buckets[window_start] = self.blank_bucket()
        self.time += 1
        return ret

    def next(self):
        pressure = self.signal(self.time)
        self.emit(self.position, pressure)
        displacement = [i*sample_length for i in self.velocity]
        self.position = map(sum, zip(self.position, displacement))
        return self.finalize_bucket()

#a = NerfSimulator((-1, -0.25, 0), (5, 0, 0), simple_cos(2000))
